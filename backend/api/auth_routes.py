from flask import Blueprint, request, jsonify, current_app
from functools import wraps
import jwt
from datetime import datetime, timedelta

# Import the data model classes from your other api files
from .user import Member
from .admin import Admin
from .employee import Employee

# A Blueprint organizes a group of related routes.
auth_bp = Blueprint('auth_bp', __name__)

def token_required(f):
    """
    Decorator to protect routes with JWT (JSON Web Token) authentication.
    It checks for a valid token in the 'Authorization' header.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            try:
                # Expects "Bearer <token>"
                token = request.headers['Authorization'].split(" ")[1]
            except IndexError:
                return jsonify({'message': 'Malformed token header!'}), 401

        if not token:
            return jsonify({'message': 'Authentication token is missing!'}), 401

        try:
            # Decode the token using the secret key from the app config
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256']) # CORRECTED ALGORITHM
            # The decoded data (user info) is passed to the route
            current_user = data
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@auth_bp.route('/register/member', methods=['POST'])
def register_member():
    """API endpoint for new gym member registration."""
    data = request.get_json()
    required_fields = ['name', 'email', 'password', 'phone_number', 'membership_plan']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    # Set a default join_date if not provided
    data['join_date'] = data.get('join_date', datetime.today().strftime('%Y-%m-%d'))

    # Use the Member.create method which handles all database logic
    new_member = Member.create(
        name=data['name'],
        email=data['email'],
        password=data['password'],
        phone_number=data['phone_number'],
        membership_plan=data['membership_plan'],
        join_date=data['join_date']
    )
    
    if new_member:
        return jsonify({
            "message": "Member registered successfully",
            "member": {"id": new_member.member_ID, "name": new_member.name, "email": new_member.email}
        }), 201  # 201 Created
    else:
        # The create method returns None if the email already exists
        return jsonify({"error": "Registration failed. Email may already be in use."}), 409  # 409 Conflict


@auth_bp.route('/login/member', methods=['POST'])
def login_member():
    """API endpoint for member login."""
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Missing email or password"}), 400

    # Use the Member.authenticate method
    member = Member.authenticate(email=data['email'], password=data['password'])
    
    if not member:
        return jsonify({"error": "Invalid credentials"}), 401

    # Create the JWT token payload
    token_payload = {
        'user_id': member.member_ID,
        'email': member.email,
        'role': 'member',
        'name': member.name, # Added name to payload
        'exp': datetime.utcnow() + timedelta(hours=24)  # Token expires in 24 hours
    }
    
    token = jwt.encode(token_payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    
    return jsonify({'message': 'Login successful', 'token': token})


@auth_bp.route('/login/admin', methods=['POST'])
def login_admin():
    """API endpoint for admin login."""
    data = request.get_json()
    # Admin login is with username, not email
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"error": "Missing username or password"}), 400

    admin = Admin.authenticate(username=data['username'], password=data['password'])
    
    if not admin:
        return jsonify({"error": "Invalid credentials"}), 401

    token_payload = {
        'user_id': admin.ad_ID, # CORRECTED: Accesses the correct attribute
        'username': admin.username,
        'name': admin.name, # Added name to payload
        'role': 'admin',
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    
    token = jwt.encode(token_payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    
    return jsonify({'message': 'Login successful', 'token': token})


@auth_bp.route('/login/employee', methods=['POST'])
def login_employee():
    """API endpoint for employee login."""
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Missing email or password"}), 400

    employee = Employee.authenticate(email=data['email'], password=data['password'])
    
    if not employee:
        return jsonify({"error": "Invalid credentials"}), 401

    token_payload = {
        'user_id': employee.user_id,
        'email': employee.email,
        'name': employee.name, # Added name to payload
        'role': employee.role, # Role can be 'IT' or 'Trainer'
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    
    token = jwt.encode(token_payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    
    return jsonify({'message': 'Login successful', 'token': token})

