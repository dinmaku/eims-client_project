#routes
from flask import request, jsonify
from .models import check_user, create_user, add_wishlist_item, get_user_wishlist, check_user_exists
from flask_jwt_extended import jwt_required, get_jwt_identity
from .db import get_db_connection
from flask_jwt_extended import create_access_token

def init_routes(app):
    @app.route('/login', methods=['POST'])
    def login():
        data = request.json
        email = data.get('email')
        password = data.get('password')

        if check_user(email, password):
            access_token = create_access_token(identity=email)  # Create a JWT token with the user's email as identity
            return jsonify({'message': 'Login successful!', 'access_token': access_token}), 200
        else:
            return jsonify({'message': 'Invalid email or password.'}), 401
            
    def get_user_id_by_email(email):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT userid FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            return user[0] if user else None
        finally:
            cursor.close()
            conn.close()
            
        

    @app.route('/register', methods=['POST'])
    def register():
        data = request.json
        first_name = data.get('firstName')
        last_name = data.get('lastName')
        email = data.get('email')
        address = data.get('address')
        contact_number = data.get('contactNumber')
        password = data.get('password')
        user_type = 'client'

        if not all([first_name, last_name, email, address, contact_number, password]):
            return jsonify({'message': 'All fields are required!'}), 400

        if create_user(first_name, last_name, email, address, contact_number, password, user_type):
            return jsonify({'message': 'Registration successful!'}), 201
        else:
            return jsonify({'message': 'Email already exists!'}), 409



        
    @app.route('/wishlist', methods=['POST'])
    @jwt_required()  # Require authentication
    def add_wishlist():
        try:
            userid = get_jwt_identity()
            data = request.json
            
            print('Received data:', data)  # Debugging line
            print('User ID from JWT:', userid)  # Debugging line

            event_name = data.get('event_name')
            event_type = data.get('event_type')
            event_theme = data.get('event_theme')
            event_color = data.get('event_color')
            venue = data.get('venue')

            print('Event Data:', event_name, event_type, event_theme, event_color, venue)  # Debugging line

            if not all([event_name, event_type, event_theme, event_color, venue]):
                return jsonify({'message': 'All fields are required!'}), 400

            if add_wishlist_item(userid, event_name, event_type, event_theme, event_color, venue):
                return jsonify({'message': 'Wishlist item added successfully'}), 201
            else:
                return jsonify({'message': 'Error adding wishlist item'}), 500
        except Exception as e:
            return jsonify({'message': str(e)}), 500  # Return any exception that occurs


    # Route to get wishlist items for logged-in user
    @app.route('/wishlist', methods=['GET'])
    @jwt_required()  # Require authentication
    def get_wishlist():
        # Get user ID from JWT
        userid = get_jwt_identity()
        wishlist = get_user_wishlist(userid)

        return jsonify(wishlist), 200


        