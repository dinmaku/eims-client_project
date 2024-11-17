#__init__.py
from flask import Flask
from flask_cors import CORS
from .routes import init_routes
import os
from flask_jwt_extended import JWTManager
00
def create_app():
    app = Flask(__name__)

    CORS(app, origins=["http://localhost:5173"], supports_credentials=True)

    # Set up the Flask-JWT-Extended configuration
    app.config['JWT_SECRET_KEY'] = os.getenv('eims', 'fallback_jwt_secret')  # Ensure you set a JWT secret key
    
     # Set JWT token expiration to 'False' to make it never expire
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False  # Disable token expiration

    # Initialize JWT manager
    jwt = JWTManager(app)

    # Initialize your routes
    init_routes(app)

    return app