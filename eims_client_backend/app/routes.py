from flask import request, jsonify, session
from .models import check_user, create_user, add_wishlist_item, get_user_wishlist
from .db import get_db_connection  # Assuming you have a function to get database connections
import logging

logging.basicConfig(level=logging.DEBUG)

def init_routes(app):
    @app.route('/login', methods=['POST'])
    def login():
        data = request.json
        email = data.get('email')
        password = data.get('password')

        if check_user(email, password):
            session['user_email'] = email  # Store the email in session
            print(f"User logged in: {email}")  # Debug statement
            return jsonify({'message': 'Login successful!'}), 200
        else:
            return jsonify({'message': 'Invalid email or password.'}), 401

    @app.route('/logout', methods=['GET'])
    def logout():
        session.pop('user_email', None)  # Clear the session
        return jsonify({'message': 'Logged out successfully'}), 200

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
    def add_wishlist():
        print("Current session:", session)  # Debug statement
        if 'user_email' not in session:
            print("Authentication required")  # Debug statement
            return jsonify({'message': 'Authentication required'}), 401

        email = session['user_email']
        userid = get_user_id_by_email(email)
        data = request.json

        event_name = data.get('event_name')
        event_type = data.get('event_type')
        event_theme = data.get('event_theme')
        event_color = data.get('event_color')
        venue = data.get('venue')

        if not all([event_name, event_type, event_theme, event_color, venue]):
            return jsonify({'message': 'All fields are required!'}), 400

        if add_wishlist_item(userid, event_name, event_type, event_theme, event_color, venue):
            return jsonify({'message': 'Wishlist item added successfully'}), 201
        else:
            return jsonify({'message': 'Error adding wishlist item'}), 500

    @app.route('/wishlist', methods=['GET'])
    def get_wishlist():
        if 'user_email' not in session:
            return jsonify({'message': 'Authentication required'}), 401

        email = session['user_email']
        userid = get_user_id_by_email(email)
        wishlist = get_user_wishlist(userid)

        return jsonify(wishlist), 200

        