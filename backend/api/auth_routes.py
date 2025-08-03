from flask import Blueprint, request, jsonify
from mysql.connector import Error
import re # For email validation
import jwt
import os
from datetime import datetime, timedelta
from functools import wraps

# Go up one directory to import from database and core
import sys
sys.path.append('..')

from database.connection import get_db_connection
from core.security import hash_password, verify_password

def token_required(f):
    """Decorator to protect routes with JWT authentication."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            # Expected format: "Bearer <token>"
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'message': 'Authentication token is missing!'}), 401

        secret_key = os.getenv('SECRET_KEY')
        try:
            # Decode the token and get the user payload
            data = jwt.decode(token, secret_key, algorithms=['HS256'])
            current_user = data
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 401

        # Pass the user data to the route
        return f(current_user, *args, **kwargs)

    return decorated

# A Blueprint is a way to organize a group of related views and other code.
# Rather than registering views and other code directly with an application,
# they are registered with a blueprint. Then the blueprint is registered
# with the application when it is available in a factory function.
auth_bp = Blueprint('auth_bp', __name__)

def is_valid_email(email):
    """Simple regex for email validation."""
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email)

@auth_bp.route('/register', methods=['POST'])
def register_user():
    """API endpoint for user registration."""
    data = request.get_json()
    if not data or not data.get('name') or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Missing required fields"}), 400

    name = data['name']
    email = data['email']
    password = data['password']
    # Default role is 'employee', can be changed to 'admin' manually in DB if needed
    role = data.get('role', 'employee') 

    if not is_valid_email(email):
        return jsonify({"error": "Invalid email format"}), 400
    
    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters long"}), 400

    hashed_pass = hash_password(password)

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    cursor = conn.cursor()

    try:
        # Check if email already exists
        cursor.execute("SELECT email FROM Users WHERE email = %s", (email,))
        if cursor.fetchone():
            return jsonify({"error": "An account with this email already exists"}), 409 # 409 Conflict

        # Insert new user
        query = "INSERT INTO Users (name, email, password, role) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (name, email, hashed_pass, role))
        conn.commit()
        
        return jsonify({"message": "User registered successfully!"}), 201

    except Error as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500
    finally:
        cursor.close()
        conn.close()


@auth_bp.route('/login', methods=['POST'])
def login_user():
    """API endpoint for user login."""
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Missing email or password"}), 400

    email = data['email']
    password = data['password']

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    # Use a dictionary cursor to get column names
    cursor = conn.cursor(dictionary=True) 

    try:
        cursor.execute("SELECT * FROM Users WHERE email = %s", (email,))
        user = cursor.fetchone()
        
        if not user:
            return jsonify({"error": "Invalid credentials"}), 401 # 401 Unauthorized

        if not verify_password(password, user['password']):
            cursor.close()
            conn.close()
            return jsonify({"error": "Invalid credentials"}), 401
        
        cursor.close()
        conn.close()

        # In a real app, you would return a JWT (JSON Web Token) here for session management
        # For now, we'll return a simple success message and user info
        user_info = {
            "user_id": user['user_id'],
            "name": user['name'],
            "role": user['role'],
            'exp': datetime.utcnow() + timedelta(hours=24) 
        }

         # Generate the token
        secret_key = os.getenv('SECRET_KEY')
        token = jwt.encode(user_info, secret_key, algorithm='HS256')

        return jsonify({'message': 'Login successful', 'token': token})

    except Error as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500
    finally:
        cursor.close()
        conn.close()
