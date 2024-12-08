# models.py

import hashlib
from .db import get_db_connection
import logging
from datetime import date, time



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_user(identifier, password):
    """
    Checks if the user exists using either email or username.
    :param identifier: email or username of the user
    :param password: plaintext password to verify
    :return: Tuple (is_valid, user_type)
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed_password = hash_password(password)

    try:
        # Check for user by email or username
        cursor.execute(
            "SELECT password, user_type FROM users WHERE email = %s OR username = %s",
            (identifier, identifier)
        )
        user = cursor.fetchone()

        # Ensure user exists and password matches
        if user and user[0] == hashed_password:
            return True, user[1]  # Return True and user_type (e.g., admin, staff, client)
        return False, None
    finally:
        cursor.close()
        conn.close()

def create_user(first_name, last_name, username, email, contact_number, password, user_type='Client', address=''):
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
            """INSERT INTO users (firstname, lastname, username, email, contactnumber, password, user_type, address)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",  # Correct number of placeholders
            (first_name, last_name, username, email, contact_number, hashed_password, user_type, address)
        )
        conn.commit()
        return True
    finally:
        cursor.close()
        conn.close()





def get_user_wishlist(userid):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT 
                e.events_id, e.event_name, e.event_type, e.event_theme, e.event_color, 
                e.schedule, e.start_time, e.end_time, e.status,
                ep.package_id, ep.package_name, ep.package_type, ep.capacity, 
                ep.description AS package_description, ep.total_price,
                v.venue_name, v.location, 
                gp.gown_package_name, gp.gown_package_price,
                array_remove(array_agg(DISTINCT CASE WHEN ps.supplier_id IS NOT NULL THEN ps.package_service_id END), NULL) AS internal_package_service_ids,
                array_remove(array_agg(DISTINCT CASE WHEN ps.supplier_id IS NOT NULL THEN ps.supplier_id END), NULL) AS internal_supplier_ids,
                array_remove(array_agg(DISTINCT CASE WHEN ps.supplier_id IS NOT NULL THEN u.firstname || ' ' || u.lastname END), NULL) AS internal_supplier_names,
                array_remove(array_agg(DISTINCT CASE WHEN ps.supplier_id IS NOT NULL THEN s.service END), NULL) AS internal_services,
                array_remove(array_agg(DISTINCT CASE WHEN ps.supplier_id IS NOT NULL THEN s.price END), NULL) AS internal_service_prices,
                array_remove(array_agg(DISTINCT CASE WHEN ps.supplier_id IS NULL THEN ps.package_service_id END), NULL) AS external_package_service_ids,
                array_remove(array_agg(DISTINCT CASE WHEN ps.supplier_id IS NULL THEN ps.external_supplier_name END), NULL) AS external_supplier_names,
                array_remove(array_agg(DISTINCT CASE WHEN ps.supplier_id IS NULL THEN ps.external_supplier_contact END), NULL) AS external_supplier_contacts,
                array_remove(array_agg(DISTINCT CASE WHEN ps.supplier_id IS NULL THEN ps.external_supplier_price END), NULL) AS external_supplier_prices,
                array_remove(array_agg(DISTINCT ps.remarks), NULL) AS remarks
            FROM events e
            LEFT JOIN event_packages ep ON e.package_id = ep.package_id
            LEFT JOIN venues v ON ep.venue_id = v.venue_id
            LEFT JOIN gown_package gp ON ep.gown_package_id = gp.gown_package_id
            LEFT JOIN event_package_services eps ON ep.package_id = eps.package_id
            LEFT JOIN package_service ps ON eps.package_service_id = ps.package_service_id
            LEFT JOIN suppliers s ON ps.supplier_id = s.supplier_id
            LEFT JOIN users u ON s.userid = u.userid
            WHERE e.userid = %s
            GROUP BY e.events_id, ep.package_id, v.venue_name, v.location, gp.gown_package_name, gp.gown_package_price
        """, (userid,))
        columns = [desc[0] for desc in cursor.description]
        wishlist = cursor.fetchall()

        # Convert the result to dictionaries and ensure time objects are strings
        result = []
        for item in wishlist:
            item_dict = dict(zip(columns, item))
            if isinstance(item_dict['start_time'], time):
                item_dict['start_time'] = item_dict['start_time'].strftime("%H:%M:%S")
            if isinstance(item_dict['end_time'], time):
                item_dict['end_time'] = item_dict['end_time'].strftime("%H:%M:%S")
            result.append(item_dict)
        
        return result
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



#package models

def get_packages():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            SELECT
                ep.package_id, ep.package_name, ep.package_type, ep.capacity, ep.description, 
                ep.gown_package_id, gp.gown_package_name, gp.gown_package_price, 
                ep.additional_capacity_charges, ep.charge_unit, ep.total_price, 
                v.venue_id, v.venue_name, v.location, v.venue_price, 
                array_agg(ps.package_service_id) AS service_ids, 
                array_agg(s.supplier_id) AS supplier_ids, 
                array_agg(s.service) AS services, 
                array_agg(s.price) AS service_prices, 
                array_agg(u.firstname) AS supplier_firstnames, 
                array_agg(u.lastname) AS supplier_lastnames, 
                array_agg(u.email) AS supplier_emails, 
                array_agg(u.contactnumber) AS supplier_contacts, 
                array_agg(ps.external_supplier_name) AS external_supplier_names, 
                array_agg(ps.external_supplier_contact) AS external_supplier_contacts, 
                array_agg(ps.external_supplier_price) AS external_supplier_prices, 
                array_agg(ps.remarks) AS remarks
            FROM event_packages ep
            LEFT JOIN gown_package gp ON ep.gown_package_id = gp.gown_package_id
            LEFT JOIN venues v ON ep.venue_id = v.venue_id
            LEFT JOIN event_package_services eps ON ep.package_id = eps.package_id
            LEFT JOIN package_service ps ON eps.package_service_id = ps.package_service_id
            LEFT JOIN suppliers s ON ps.supplier_id = s.supplier_id
            LEFT JOIN users u ON s.userid = u.userid
            GROUP BY ep.package_id, gp.gown_package_id, v.venue_id
            """
        )
        packages = cursor.fetchall()
        return [
            {
                'package_id': item[0],
                'package_name': item[1],
                'package_type': item[2],
                'capacity': item[3],
                'description': item[4],
                'gown_package_id': item[5],
                'gown_package_name': item[6],
                'gown_package_price': item[7],
                'additional_capacity_charges': item[8],
                'charge_unit': item[9],
                'total_price': item[10],
                'venue_id': item[11],
                'venue_name': item[12],
                'venue_location': item[13],
                'venue_price': item[14],
                'package_service_ids': item[15],
                'supplier_ids': item[16],
                'services': item[17],
                'service_prices': item[18],
                'supplier_firstnames': item[19],
                'supplier_lastnames': item[20],
                'supplier_emails': item[21],
                'supplier_contacts': item[22],
                'external_supplier_names': item[23],
                'external_supplier_contacts': item[24],
                'external_supplier_prices': item[25],
                'remarks': item[26],
            }
            for item in packages
        ]
    finally:
        cursor.close()
        conn.close()



def get_package_details_by_id(package_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT ep.package_id, ep.package_name, ep.package_type, ep.capacity, ep.description, ep.total_price,
                   ep.additional_capacity_charges, ep.charge_unit,  -- Added fields
                   v.venue_name, v.location, v.venue_price,
                   gp.gown_package_name, gp.gown_package_price,
                   array_agg(ps.package_service_id) AS package_service_ids,
                   array_agg(ps.supplier_id) AS supplier_ids,
                   array_agg(s.service) AS services,
                   array_agg(s.price) AS service_prices,
                   array_agg(ps.external_supplier_name) AS external_supplier_names,
                   array_agg(ps.external_supplier_contact) AS external_supplier_contacts,
                   array_agg(ps.external_supplier_price) AS external_supplier_prices,
                   array_agg(ps.remarks) AS remarks
            FROM event_packages ep
            LEFT JOIN venues v ON ep.venue_id = v.venue_id
            LEFT JOIN gown_package gp ON ep.gown_package_id = gp.gown_package_id
            LEFT JOIN event_package_services eps ON ep.package_id = eps.package_id
            LEFT JOIN package_service ps ON eps.package_service_id = ps.package_service_id
            LEFT JOIN suppliers s ON ps.supplier_id = s.supplier_id
            WHERE ep.package_id = %s
            GROUP BY ep.package_id, v.venue_name, v.location, v.venue_price, gp.gown_package_name, gp.gown_package_price
        """, (package_id,))
        columns = [desc[0] for desc in cursor.description]
        package = cursor.fetchone()
        return dict(zip(columns, package)) if package else None
    finally:
        cursor.close()
        conn.close()




def add_event_item(userid, event_name, event_type, event_theme, event_color, package_id, suppliers, total_price, schedule=None, start_time=None, end_time=None, status='Wishlist'):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("BEGIN")

        # Update the total_price in the event_packages table
        cursor.execute("""
            UPDATE event_packages
            SET total_price = %s
            WHERE package_id = %s
        """, (total_price, package_id))

        # Insert into events table
        cursor.execute("""
            INSERT INTO events (userid, event_name, event_type, event_theme, event_color, package_id, schedule, start_time, end_time, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING events_id
        """, (userid, event_name, event_type, event_theme, event_color, package_id, schedule, start_time, end_time, status))
        events_id = cursor.fetchone()[0]

        # Insert suppliers into package_service table and link them to event_package_services
        for supplier in suppliers:
            if supplier['type'] == 'internal':
                cursor.execute("""
                    INSERT INTO package_service (supplier_id, remarks)
                    VALUES (%s, %s) RETURNING package_service_id
                """, (supplier.get('supplier_id'), supplier.get('remarks', '')))
            else:
                cursor.execute("""
                    INSERT INTO package_service (external_supplier_name, external_supplier_contact, external_supplier_price, remarks)
                    VALUES (%s, %s, %s, %s) RETURNING package_service_id
                """, (supplier.get('external_supplier_name'), supplier.get('external_supplier_contact'), supplier.get('external_supplier_price'), supplier.get('remarks', '')))
            
            package_service_id = cursor.fetchone()[0]
            
            # Link the package_service to the event_package
            cursor.execute("""
                INSERT INTO event_package_services (package_id, package_service_id)
                VALUES (%s, %s)
            """, (package_id, package_service_id))

        cursor.execute("COMMIT")
        return events_id
    except Exception as e:
        cursor.execute("ROLLBACK")
        print(f"Error adding event item: {e}")
        return None
    finally:
        cursor.close()
        conn.close()



        





def get_user_id_by_email(email):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT userid FROM users WHERE email = %s", (email,))
        result = cursor.fetchone()
        return result[0] if result else None
    finally:
        cursor.close()
        conn.close()

def get_available_suppliers():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT s.supplier_id, u.firstname, u.lastname, s.service, s.price
            FROM suppliers s
            JOIN users u ON s.userid = u.userid
        """)
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    finally:
        cursor.close()
        conn.close()

def get_available_venues():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT venue_id, venue_name, location, venue_price FROM venues")
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    finally:
        cursor.close()
        conn.close()

def get_available_gown_packages():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT gown_package_id, gown_package_name, gown_package_price FROM gown_package")
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    finally:
        cursor.close()
        conn.close()