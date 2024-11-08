#routes.py
from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .models import check_user, create_user, add_wishlist_item, get_user_wishlist, get_user_id_by_email
import logging
import jwt
from functools import wraps
import os

logging.basicConfig(level=logging.DEBUG)

def init_routes(app):
    
    @app.route('/login', methods=['POST'])
    def login():
        try:
            # Get the login data
            data = request.json
            email = data.get('email')
            password = data.get('password')

            # Check if email and password are provided
            if not email or not password:
                print("Missing email or password")
                return jsonify({'message': 'Email and password are required!'}), 400

            # Check the user credentials
            if check_user(email, password):
                # Generate JWT token
                access_token = create_access_token(identity=email)

                return jsonify({
                    'message': 'Login successful!',
                    'access_token': access_token
                }), 200
            else:
                print("Invalid credentials")
                return jsonify({'message': 'Invalid email or password.'}), 401

        except Exception as e:
            print(f"Error during login: {e}")
            return jsonify({'message': 'An error occurred during login.'}), 500

    @app.route('/register', methods=['POST'])
    def register():
        data = request.json
        first_name = data.get('firstName')
        last_name = data.get('lastName')
        email = data.get('email')
        address = data.get('address')
        contact_number = data.get('contactNumber')
        password = data.get('password')
        user_type = 'client'  # Default user type

        # Validate required fields
        if not all([first_name, last_name, email, address, contact_number, password]):
            return jsonify({'message': 'All fields are required!'}), 400

        # Attempt to create the user
        if create_user(first_name, last_name, email, address, contact_number, password, user_type):
            return jsonify({'message': 'Registration successful!'}), 201
        else:
            return jsonify({'message': 'Email already exists!'}), 409

    @app.route('/wishlist', methods=['POST'])
    @jwt_required()
    def add_wishlist():
        email = get_jwt_identity()
        userid = get_user_id_by_email(email)
        data = request.json

        event_name = data.get('event_name')
        event_type = data.get('event_type')
        event_theme = data.get('event_theme')
        event_color = data.get('event_color')
        venue = data.get('venue')

        # Log the incoming data to check if it's being sent correctly
        app.logger.debug(f"Received data: {data}")

        if not all([event_name, event_type, event_theme, event_color, venue]):
            return jsonify({'message': 'All fields are required!'}), 400

        if add_wishlist_item(userid, event_name, event_type, event_theme, event_color, venue):
            return jsonify({'message': 'Wishlist item added successfully'}), 201
        else:
            return jsonify({'message': 'Error adding wishlist item'}), 500

    @app.route('/wishlist', methods=['GET'])
    @jwt_required()
    def get_wishlist():
        email = get_jwt_identity()
        userid = get_user_id_by_email(email)
        wishlist = get_user_wishlist(userid)

        return jsonify(wishlist), 200
    
    SECRET_KEY = os.getenv('eims', 'fallback_jwt_secret')

# Decorator to protect routes and check token
    def token_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({'msg': 'Token is missing'}), 403

            try:
                # Remove 'Bearer ' from the token string
                token = token.split(" ")[1]
                # Decode the token using the secret key
                decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                return jsonify({'msg': 'Token has expired'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'msg': 'Invalid token'}), 401

            # Token is valid, pass control to the original route function
            return f(decoded_token, *args, **kwargs)

        return decorated_function
    
    @app.route('/check-auth', methods=['GET'])
    @jwt_required()
    def check_auth():
        try:
            # Access the identity from the decoded JWT token
            current_user = get_jwt_identity()  # This is the email (identity) you set in the JWT token
            return jsonify({"msg": f"Token is valid for user: {current_user}"}), 200
        except Exception as e:
            return jsonify({'msg': f'Error: {str(e)}'}), 422
        
    @app.route('/refresh', methods=['POST'])
    @jwt_required(refresh=True)
    def refresh():
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user)
        return jsonify(access_token=new_access_token)


    @app.route('/logout', methods=['POST'])
    def logout():
        # No need to clear session in JWT-based auth, just inform the client to delete the token
        return jsonify({'message': 'Logged out successfully'}), 200
    


