#__init__.py
from flask import Flask, session
from flask_cors import CORS
from .routes import init_routes

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Set the secret key for sessions
    app.config['SECRET_KEY'] = 'eims'  # Make sure this is a strong key

    # Set the session cookie settings if needed
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SECURE'] = False  # Set to True if using HTTPS

    # Initialize your routes
    init_routes(app)

    return app
