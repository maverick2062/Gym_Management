from flask import Flask, jsonify
from flask_cors import CORS
import os

# Import the blueprints from the api folder
from api.auth_routes import auth_bp
from api.member_routes import member_bp
from api.employee_routes import employee_bp
from api.equipment_routes import equipment_bp

# Import the database setup function
from database.connection import setup_database

# --- Database Setup ---
# This command will run when the application starts, ensuring the database
# and all necessary tables are created before the server accepts requests.
setup_database()
# --------------------

# Create the Flask app
app = Flask(__name__)

# Load secret key from environment variables for JWT
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'a_default_fallback_secret_key')

# Enable CORS (Cross-Origin Resource Sharing)
CORS(app)

# A simple test route to make sure the server is running
@app.route('/api/ping', methods=['GET'])
def ping_pong():
    return jsonify({"message": "pong!"}), 200

# Register the blueprints with their respective URL prefixes
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(member_bp, url_prefix='/api/members')
app.register_blueprint(employee_bp, url_prefix='/api/employees')
app.register_blueprint(equipment_bp, url_prefix='/api/equipment')


if __name__ == '__main__':
    # The server will run on http://127.0.0.1:5000
    # The debug=True flag allows the server to auto-reload when you save changes
    app.run(debug=True, port=5000)
