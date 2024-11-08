#__init__.py
from flask import Flask
from flask_cors import CORS
from .routes import init_routes
from flask import session, redirect, url_for
import os


def create_app():
    app = Flask(__name__)

    CORS(app, origins=["http://localhost:5173"], supports_credentials=True)

    # Set the secret key for sessions
    app.config['SECRET_KEY'] = os.getenv('eims', 'fallback_secret')

    # Set the session cookie settings if needed
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_COOKIE_SECURE'] = True  # Set to True if using HTTPS
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_NAME'] = 'session'
    app.config['SESSION_TYPE'] = 'filesystem'

    # Initialize your routes
    init_routes(app)

    return app
