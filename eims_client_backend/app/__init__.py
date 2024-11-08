#__init__.py
from flask import Flask
from flask_cors import CORS
from .routes import init_routes
import os
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)

    CORS(app, origins=["http://localhost:5173"], supports_credentials=True)

    # Set up the Flask-JWT-Extended configuration
    app.config['JWT_SECRET_KEY'] = os.getenv('eims', 'fallback_jwt_secret')  # Ensure you set a JWT secret key

    # Initialize JWT manager
    jwt = JWTManager(app)

    # Initialize your routes
    init_routes(app)

    return app