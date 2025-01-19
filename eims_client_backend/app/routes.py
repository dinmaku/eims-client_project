#routes.py
from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .models import (
    check_user, create_user, get_user_wishlist, 
    get_user_id_by_email, create_outfit, get_outfits, get_outfit_by_id, 
    book_outfit, get_booked_wishlist_by_user, delete_booked_wishlist, 
    get_package_details_by_id, get_booked_outfits_by_user, get_packages, 
    get_available_suppliers, get_available_venues, get_available_gown_packages, 
    get_event_types, get_all_additional_services, get_booked_schedules, add_event_item,
    create_wishlist_package, initialize_test_suppliers
)
import logging
import jwt
from functools import wraps
import os
from datetime import datetime, date, time

logging.basicConfig(level=logging.DEBUG)

def init_routes(app):
    
    @app.route('/login', methods=['POST'])
    def login():
        try:
            # Get the login data
            data = request.json
            identifier = data.get('identifier')  # Can be email or username
            password = data.get('password')

            # Check if identifier and password are provided
            if not identifier or not password:
                return jsonify({'message': 'Username/Email and password are required!'}), 400

            # Check the user credentials
            is_valid, user_type = check_user(identifier, password)
            if is_valid:
                # Generate JWT token with additional claims
                access_token = create_access_token(identity=identifier, additional_claims={"user_type": user_type})

                return jsonify({
                    'message': 'Login successful!',
                    'access_token': access_token,
                    'user_type': user_type
                }), 200
            else:
                return jsonify({'message': 'Invalid username/email or password.'}), 401

        except Exception as e:
            print(f"Error during login: {e}")
            return jsonify({'message': 'An error occurred during login.'}), 500



    @app.route('/register', methods=['POST'])
    def register():
        data = request.json
        print(data)  # Log the incoming data for debugging
        first_name = data.get('firstName')
        last_name = data.get('lastName')
        username = data.get('username')
        email = data.get('email')
        contact_number = data.get('contactNumber')
        password = data.get('password')
        address = data.get('address', '') 
        user_type = 'Client'  # Default user type

        # Validate required fields
        if not all([first_name, last_name, username, email, contact_number, password]):
            return jsonify({'message': 'All fields are required!'}), 400

        # Attempt to create the user
        if create_user(first_name, last_name, username, email, contact_number, password, user_type, address):
            return jsonify({'message': 'Registration successful!'}), 201
        else:
            return jsonify({'message': 'Email already exists!'}), 409





    @app.route('/available-suppliers', methods=['GET'])
    @jwt_required()
    def get_available_suppliers_route():
        try:
            suppliers = get_available_suppliers()
            return jsonify(suppliers), 200
        except Exception as e:
            app.logger.error(f"Error fetching available suppliers: {e}")
            return jsonify({'message': 'An error occurred while fetching available suppliers'}), 500

    @app.route('/available-venues', methods=['GET'])
    @jwt_required()
    def get_available_venues_route():
        try:
            venues = get_available_venues()
            return jsonify(venues), 200
        except Exception as e:
            app.logger.error(f"Error fetching available venues: {e}")
            return jsonify({'message': 'An error occurred while fetching available venues'}), 500

    @app.route('/available-gown-packages', methods=['GET'])
    @jwt_required()
    def get_available_gown_packages_route():
        try:
            gown_packages = get_available_gown_packages()
            return jsonify(gown_packages), 200
        except Exception as e:
            app.logger.error(f"Error fetching available gown packages: {e}")
            return jsonify({'message': 'An error occurred while fetching available gown packages'}), 500

    @app.route('/packages/<int:package_id>', methods=['GET'])
    @jwt_required()
    def get_package_details(package_id):
        try:
            package = get_package_details_by_id(package_id)  # Implement this function to fetch package details
            if not package:
                return jsonify({'message': 'Package not found'}), 404
            return jsonify(package), 200
        except Exception as e:
            app.logger.error(f"Error fetching package details: {e}")
            return jsonify({'message': 'An error occurred while fetching package details'}), 500




    @app.route('/wishlist', methods=['GET'])
    @jwt_required()
    def get_wishlist():
        email = get_jwt_identity()
        userid = get_user_id_by_email(email)
        print(f"User ID from email: {userid}")  # Debug statement
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
       
        return jsonify({'message': 'Logged out successfully'}), 200

    @app.route('/outfits', methods=['POST'])
    @jwt_required()
    def add_outfit():
        try:
            data = request.json
            outfit_name = data.get('outfit_name')
            outfit_type = data.get('outfit_type')
            outfit_color = data.get('outfit_color')
            outfit_desc = data.get('outfit_desc')
            rent_price = data.get('rent_price')
            status = data.get('status')
            outfit_img = data.get('outfit_img')

            # Validate required fields
            if not all([outfit_name, outfit_type, outfit_color, outfit_desc, rent_price, status, outfit_img]):
                return jsonify({'message': 'All fields are required!'}), 400

            # Create the new outfit
            if create_outfit(outfit_name, outfit_type, outfit_color, outfit_desc, rent_price, status, outfit_img):
                return jsonify({'message': 'Outfit added successfully!'}), 201
            else:
                return jsonify({'message': 'Error adding outfit'}), 500
        except Exception as e:
            return jsonify({'message': f'Error: {str(e)}'}), 500

    @app.route('/outfits', methods=['GET'])
    @jwt_required()
    def get_all_outfits():
        try:
            outfits = get_outfits()
            return jsonify(outfits), 200
        except Exception as e:
            return jsonify({'message': f'Error fetching outfits: {str(e)}'}), 500

    @app.route('/outfits/<int:outfit_id>', methods=['GET'])
    @jwt_required()
    def get_outfit(outfit_id):
        try:
            outfit = get_outfit_by_id(outfit_id)
            if outfit:
                return jsonify(outfit), 200
            else:
                return jsonify({'message': 'Outfit not found'}), 404
        except Exception as e:
            return jsonify({'message': f'Error fetching outfit: {str(e)}'}), 500

    @app.route('/book-outfit', methods=['POST'])
    @jwt_required()
    def book_outfit_route():
        try:
            email = get_jwt_identity()
            userid = get_user_id_by_email(email)  # Assuming this function exists

            data = request.json
            outfit_id = data.get('outfit_id')
            pickup_date = data.get('pickup_date')
            return_date = data.get('return_date')
            status = data.get('status')
            additional_charges = data.get('additional_charges', 0)

            if book_outfit(userid, outfit_id, pickup_date, return_date, status, additional_charges):
                return jsonify({'message': 'Outfit booked successfully!'}), 201
            else:
                return jsonify({'message': 'Error booking outfit'}), 500
        except Exception as e:
            return jsonify({'message': f'Error booking outfit: {str(e)}'}), 500

      
    @app.route('/booked-wishlist', methods=['GET'])
    @jwt_required()
    def get_user_booked_wishlist():
        try:
            email = get_jwt_identity()
            userid = get_user_id_by_email(email)  # Assuming a function to get user ID by email exists

            # Fetch events for the user from the updated events table
            booked_wishlist = get_booked_wishlist_by_user(userid)
            return jsonify(booked_wishlist), 200
        except Exception as e:
            return jsonify({'message': f'Error fetching booked wishlist: {str(e)}'}), 500


    @app.route('/booked_wishlist/<int:events_id>', methods=['DELETE'])
    @jwt_required()  # Assuming you're using JWT for authorization
    def delete_wishlist_item(events_id):
        try:
            # Call the function to delete the event item by events_id
            if delete_booked_wishlist(events_id):
                return jsonify({"message": "Event item deleted successfully"}), 200
            else:
                return jsonify({"message": "Failed to delete event item"}), 500
        except Exception as e:
            return jsonify({"message": f"Error: {str(e)}"}), 500

    @app.route('/booked-outfits', methods=['GET'])
    @jwt_required()
    def get_user_booked_outfits():
        try:
            # Fetch the current user's email from the JWT token
            email = get_jwt_identity()
            
            # Here, you would fetch the user's ID based on their email (you can create a helper function for this)
            # Assuming you have a function to get the user ID from email
            userid = get_user_id_by_email(email)
            
            # Fetch the booked outfits for the user
            booked_outfits = get_booked_outfits_by_user(userid)
            
            # Return the fetched data as JSON
            return jsonify(booked_outfits), 200
        except Exception as e:
            # If there's an error, return a message with the error details
            return jsonify({'message': f'Error fetching booked outfits: {str(e)}'}), 500


    #packages routes
    @app.route('/created-packages', methods=['GET'])
    @jwt_required()
    def get_packages_route():
        try:
            # Fetch all event packages
            packages = get_packages()
            return jsonify(packages), 200
        except Exception as e:
            app.logger.error(f"Error fetching packages: {e}")
            return jsonify({'message': 'An error occurred while fetching packages'}), 500


    @app.route('/event-types', methods=['GET'])
    def get_event_types_route():
        try:
            event_types = get_event_types()
            return jsonify(event_types), 200
        except Exception as e:
            app.logger.error(f"Error fetching event types: {e}")
            return jsonify({"error": str(e)}), 500


    #additional services routes

    @app.route('/created-services', methods=['GET'])
    @jwt_required()
    def get_services_route():
        try:
            services = get_all_additional_services()
            return jsonify(services), 200
        except Exception as e:
            app.logger.error(f"Error fetching services: {e}")
            return jsonify({'message': 'An error occurred while fetching services'}), 500

    @app.route('/api/events/schedules', methods=['GET'])
    @jwt_required()
    def get_booked_schedules_route():
        try:
            schedules = get_booked_schedules()
            return jsonify(schedules)
        except Exception as e:
            app.logger.error(f"Error in get_booked_schedules route: {str(e)}")
            return jsonify({'error': str(e)}), 422



    @app.route('/events', methods=['POST', 'OPTIONS'])
    @jwt_required()
    def create_event():
        if request.method == 'OPTIONS':
            # Handle preflight request
            response = jsonify({'message': 'OK'})
            response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            response.headers.add('Access-Control-Allow-Methods', 'POST,OPTIONS')
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            return response, 200
            
        try:
            # Get user ID from JWT token
            email = get_jwt_identity()
            userid = get_user_id_by_email(email)
            
            if not userid:
                response = jsonify({
                    'success': False,
                    'message': 'Invalid user token'
                })
                response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
                response.headers.add('Access-Control-Allow-Credentials', 'true')
                return response, 401

            data = request.get_json()
            
            # Extract base event data
            event_data = {
                'userid': userid,  # Use the userid from JWT token
                'event_name': data.get('event_name'),
                'event_type': data.get('event_type'),
                'event_theme': data.get('event_theme'),
                'event_color': data.get('event_color'),
                'package_id': data.get('package_id'),
                'schedule': data.get('schedule'),
                'start_time': data.get('start_time'),
                'end_time': data.get('end_time'),
                'status': data.get('status', 'Wishlist'),
                'total_price': data.get('total_price', 0)
            }

            # Package configuration data
            package_config = {
                'suppliers': data.get('suppliers', []),
                'outfits': data.get('outfits', []),
                'services': data.get('services', []),
                'additional_items': data.get('additional_items', [])
            }

            # Add event and its configurations
            events_id = add_event_item(**event_data, **package_config)

            if events_id:
                response = jsonify({
                    'success': True,
                    'message': 'Event created successfully',
                    'events_id': events_id
                })
                response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
                response.headers.add('Access-Control-Allow-Credentials', 'true')
                return response, 201
            else:
                response = jsonify({
                    'success': False,
                    'message': 'Failed to create event'
                })
                response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
                response.headers.add('Access-Control-Allow-Credentials', 'true')
                return response, 500

        except Exception as e:
            app.logger.error(f"Error creating event: {str(e)}")
            response = jsonify({
                'success': False,
                'message': f'Error creating event: {str(e)}'
            })
            response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            return response, 500



    @app.route('/wishlist-packages', methods=['POST', 'OPTIONS'])
    @jwt_required()
    def create_wishlist_package_route():
        if request.method == 'OPTIONS':
            # Handle preflight request
            response = jsonify({'message': 'OK'})
            response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            response.headers.add('Access-Control-Allow-Methods', 'POST,OPTIONS')
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            return response, 200
            
        try:
            # Get user ID from token
            email = get_jwt_identity()
            userid = get_user_id_by_email(email)
            
            if userid is None:
                response = jsonify({
                    'success': False,
                    'message': 'User not found'
                })
                response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
                response.headers.add('Access-Control-Allow-Credentials', 'true')
                return response, 404

            data = request.get_json()

            # Create wishlist package and its related data
            wishlist_id = create_wishlist_package(
                events_id=data.get('events_id'),
                package_data=data
            )

            if wishlist_id:
                response = jsonify({
                    'success': True,
                    'message': 'Wishlist package created successfully',
                    'wishlist_id': wishlist_id
                })
                response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
                response.headers.add('Access-Control-Allow-Credentials', 'true')
                return response, 201
            else:
                response = jsonify({
                    'success': False,
                    'message': 'Failed to create wishlist package'
                })
                response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
                response.headers.add('Access-Control-Allow-Credentials', 'true')
                return response, 500

        except Exception as e:
            app.logger.error(f"Error creating wishlist package: {str(e)}")
            response = jsonify({
                'success': False,
                'message': f'Error creating wishlist package: {str(e)}'
            })
            response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            return response, 500

    @app.route('/api/suppliers', methods=['GET'])
    def get_suppliers():
        try:
            suppliers = get_available_suppliers()
            response = jsonify({
                'status': 'success',
                'data': suppliers
            })
            response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            return response, 200
        except Exception as e:
            logging.error(f"Error fetching suppliers: {e}")
            response = jsonify({
                'status': 'error',
                'message': str(e)
            })
            response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            return response, 500

    @app.route('/api/init-test-suppliers', methods=['POST'])
    def init_test_suppliers():
        try:
            success = initialize_test_suppliers()
            if success:
                return jsonify({
                    'status': 'success',
                    'message': 'Test suppliers initialized successfully'
                }), 200
            else:
                return jsonify({
                    'status': 'error',
                    'message': 'Failed to initialize test suppliers'
                }), 500
        except Exception as e:
            logging.error(f"Error initializing test suppliers: {e}")
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500