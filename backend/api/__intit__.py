from flask import Flask
from .auth_routes import auth_bp
from .member_routes import member_bp 

def create_app():
    app = Flask(__name__)
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(member_bp, url_prefix='/api/members')
    
    return app