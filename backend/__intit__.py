from flask import Flask
from .api.auth_routes import auth_bp
from .api.member_routes import member_bp # <--- ADD THIS LINE

def create_app():
    app = Flask(__name__)
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(member_bp, url_prefix='/api/members')
    
    return app