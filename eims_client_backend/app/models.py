# models.py

import hashlib
from .db import get_db_connection
import logging
from datetime import date


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_user(email, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    
    try:
        # Fetch the user entry
        cursor.execute("SELECT password, user_type FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        
        # Ensure user exists and password matches
        if user and user[0] == hashed_password:
            return True, user[1]  # Return True and user_type (e.g., admin, staff, client)
        return False, None
    finally:
        cursor.close()
        conn.close()

def create_user(first_name, last_name, email, contact_number, password, user_type='client', country=None, city=None, street=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    
    try:
        # Check if email exists
        cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            return False  # Email exists
        
        # Insert new user
        cursor.execute(
            """INSERT INTO users (firstname, lastname, email, contactnumber, password, user_type, country, city, street)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",  # 9 placeholders, matching the 9 values
            (first_name, last_name, email, contact_number, hashed_password, user_type, country, city, street)
        )
        conn.commit()
        return True
    finally:
        cursor.close()
        conn.close()


def add_event_item(userid, event_name, event_type, event_theme, event_color, venue, schedule=None, start_time=None, end_time=None, status='wishlist'):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO events (userid, event_name, event_type, event_theme, event_color, venue, schedule, start_time, end_time, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING events_id
            """,
            (userid, event_name, event_type, event_theme, event_color, venue, schedule, start_time, end_time, status)
        )
        events_id = cursor.fetchone()[0]  # Fetch the generated events_id
        conn.commit()
        return events_id  # Return the events_id
    except Exception as e:
        logger.error(f"Error adding event item: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()


def get_user_wishlist(userid):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            SELECT wishlist_id, event_name, event_type, event_theme, event_color, venue
            FROM wishlist
            WHERE userid = %s
            """,
            (userid,)
        )
        wishlist = cursor.fetchall()
        # Transform the result into a list of dictionaries
        return [
            {
                'wishlist_id': item[0],
                'event_name': item[1],
                'event_type': item[2],
                'event_theme': item[3],
                'event_color': item[4],
                'venue': item[5],
            }
            for item in wishlist
        ]
    finally:
        cursor.close()
        conn.close()


def add_event_entry(wishlist_id, schedule, start_time, end_time, status):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO events (wishlist_id, schedule, start_time, end_time, status)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (wishlist_id, schedule, start_time, end_time, status)
        )
        conn.commit()
        return True
    except Exception as e:
        # Use logger instead of app.logger
        logger.error(f"Error adding event: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()
    
        

def check_user_exists(userid):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT userid FROM users WHERE userid = %s", (userid,))
        user = cursor.fetchone()
        return user is not None
    finally:
        cursor.close()
        conn.close()


def get_user_id_by_email(email):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT userid FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        if user:
            return user[0]
        else:
            logger.warning(f"No user found with email: {email}")
            return None
    except Exception as e:
        logger.error(f"Error retrieving user ID for email {email}: {str(e)}")
        return None
    finally:
        cursor.close()
        conn.close()

        # Outfit Model
def create_outfit(outfit_name, outfit_type, outfit_color, outfit_desc, rent_price, status, outfit_img):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO outfits (outfit_name, outfit_type, outfit_color, outfit_desc, rent_price, status, outfit_img)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (outfit_name, outfit_type, outfit_color, outfit_desc, rent_price, status, outfit_img))
        conn.commit()
        return True
    except Exception as e:
        logger.error(f"Error creating outfit: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

# Outfit Archive Model
def create_outfit_archive(outfit_id, creation_address, creation_date, owner, retail_price):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO outfit_archive (outfit_id, creation_address, creation_date, owner, retail_price)
            VALUES (%s, %s, %s, %s, %s)
        """, (outfit_id, creation_address, creation_date, owner, retail_price))
        conn.commit()
        return True
    except Exception as e:
        logger.error(f"Error creating outfit archive: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

# Booked Outfit Model
def book_outfit(userid, outfit_id, pickup_date, return_date, status, additional_charges):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO booked_outfit (userid, outfit_id, pickup_date, return_date, status, additional_charges)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (userid, outfit_id, pickup_date, return_date, status, additional_charges))
        conn.commit()
        return True
    except Exception as e:
        logger.error(f"Error booking outfit: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

# Fetch outfits
def get_outfits():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM outfits")
        outfits = cursor.fetchall()
        if outfits:
            return [
                {
                    'outfit_id': item[0],
                    'outfit_name': item[1],
                    'outfit_type': item[2],
                    'outfit_color': item[3],
                    'outfit_desc': item[4],
                    'rent_price': item[5],
                    'status': item[6],
                    'outfit_img': item[7],
                    'size': item[8],
                    'weight': item[9],
                }
                for item in outfits
            ]
        else:
            return []  # No outfits found
    except Exception as e:
        logger.error(f"Error fetching outfits: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

# Fetch a specific outfit by ID
def get_outfit_by_id(outfit_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM outfits WHERE outfit_id = %s", (outfit_id,))
        outfit = cursor.fetchone()
        if outfit:
            return {
                'outfit_id': outfit[0],
                'outfit_name': outfit[1],
                'outfit_type': outfit[2],
                'outfit_color': outfit[3],
                'outfit_desc': outfit[4],
                'rent_price': outfit[5],
                'status': outfit[6],
                'outfit_img': outfit[7],
            }
        return None
    finally:
        cursor.close()
        conn.close()

# Fetch wishlist by users
def get_booked_wishlist_by_user(userid):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT events_id, userid, event_name, event_type, event_theme, event_color, venue, schedule, start_time, end_time, status
            FROM events
            WHERE userid = %s
        """, (userid,))
        events = cursor.fetchall()
        if events:
            return [
                {
                    'events_id': item[0],
                    'userid': item[1],
                    'event_name': item[2],
                    'event_type': item[3],
                    'event_theme': item[4],
                    'event_color': item[5],
                    'venue': item[6],
                    'schedule': item[7],
                    'start_time': item[8],
                    'end_time': item[9],
                    'status': item[10]
                }
                for item in events
            ]
        else:
            return []  # No events found for the user
    except Exception as e:
        logger.error(f"Error fetching events for user {userid}: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

# Delete wishlist and related events
def delete_booked_wishlist(events_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # First, delete related events (to avoid foreign key violation)
        cursor.execute("""DELETE FROM events WHERE events_id = %s""", (events_id,))
        conn.commit()

        return True
    except Exception as e:
        logger.error(f"Error deleting event item {events_id}: {e}")
        conn.rollback()  # Rollback in case of error
        return False
    finally:
        cursor.close()
        conn.close()



def get_booked_outfits():
    conn = get_db_connection()  # Assuming you have a function to get the DB connection
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM booked_outfit")
        booked_outfits = cursor.fetchall()
        
        if booked_outfits:
            return [
                {
                    'outfit_booked_id': item[0],
                    'userid': item[1],
                    'outfit_id': item[2],
                    'pickup_date': item[3],
                    'return_date': item[4],
                    'status': item[5],
                    'additional_charges': item[6]
                }
                for item in booked_outfits
            ]
        else:
            return []  # No booked outfits found
    except Exception as e:
        logger.error(f"Error fetching booked outfits: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def get_booked_outfits_by_user(userid):
    booked_outfits = get_booked_outfits()
    return [outfit for outfit in booked_outfits if outfit['userid'] == userid]



