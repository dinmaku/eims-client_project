#__init__.py
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from .routes import init_routes

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Set the secret key for JWT
    app.config['JWT_SECRET_KEY'] = 'eims'  # Use your secret key

    # Initialize JWT manager
    jwt = JWTManager(app)

    # Initialize your routes
    init_routes(app)

    return app