#__init__.py
from flask import Flask
from flask_cors import CORS
from .routes import init_routes
import os
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__, static_url_path='/static', static_folder='static')

    # Update CORS configuration to allow access to static files and all preflight requests
    CORS(app, 
         origins=["http://localhost:5173"], 
         supports_credentials=True,
         expose_headers=["Content-Type", "Authorization"],
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         resources={
             r"/static/*": {"origins": "*"},
             r"/api/*": {"origins": ["http://localhost:5173"]},
             r"/*": {"origins": ["http://localhost:5173"]}  # Add this to handle all routes
         })

    # Set up the Flask-JWT-Extended configuration
    app.config['JWT_SECRET_KEY'] = os.getenv('eims', 'fallback_jwt_secret')  # Ensure you set a JWT secret key
    
    # Set JWT token expiration to 'False' to make it never expire
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False  # Disable token expiration

    # Add these configurations to your Flask app setup
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
    app.config['PROFILE_PICTURES_FOLDER'] = os.path.join(app.config['UPLOAD_FOLDER'], 'profile_pics')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

    # Create the upload folders if they don't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['PROFILE_PICTURES_FOLDER'], exist_ok=True)

    # Initialize JWT manager
    jwt = JWTManager(app)

    # Initialize your routes
    init_routes(app)

    return app