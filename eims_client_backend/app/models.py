# models.py

import hashlib
from .db import get_db_connection

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_user(email, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    
    try:
        cursor.execute("SELECT password FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        return user and user[0] == hashed_password
    finally:
        cursor.close()
        conn.close()

def create_user(first_name, last_name, email, address, contact_number, password, user_type='client'):
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
            "INSERT INTO users (firstname, lastname, email, address, contactnumber, password, user_type) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (first_name, last_name, email, address, contact_number, hashed_password, user_type)
        )
        conn.commit()
        return True
    finally:
        cursor.close()
        conn.close()

def add_wishlist_item(userid, event_name, event_type, event_theme, event_color, venue):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(""" 
            INSERT INTO wishlist (userid, event_name, event_type, event_theme, event_color, venue)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (userid, event_name, event_type, event_theme, event_color, venue))
        conn.commit()
        return True
    except Exception as e:
        print("Error in adding wishlist item:", e)  # Log specific database errors
        return False
    finally:
        cursor.close()
        conn.close()

# Method to get wishlist items for a user
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
