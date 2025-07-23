from flask import Flask, jsonify
from flask_cors import CORS

# Import your routes here later
# from api.auth_routes import auth_bp
# from api.member_routes import member_bp

# Create the Flask app
app = Flask(__name__)

# Enable CORS (Cross-Origin Resource Sharing) to allow your frontend
# to communicate with this backend.
CORS(app)

# A simple test route to make sure the server is running
@app.route('/api/ping', methods=['GET'])
def ping_pong():
    return jsonify({"message": "pong!"}), 200

# We will register our blueprints (routes) here later
# app.register_blueprint(auth_bp, url_prefix='/api/auth')
# app.register_blueprint(member_bp, url_prefix='/api/members')


if __name__ == '__main__':
    # The server will run on http://127.0.0.1:5000
    # The debug=True flag allows the server to auto-reload when you save changes
    app.run(debug=True, port=5000)
