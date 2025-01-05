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
            WITH outfit_details AS (
                SELECT 
                    gpo.gown_package_id,
                    array_agg(o.outfit_id ORDER BY o.outfit_id) as outfit_ids,
                    array_agg(o.outfit_name ORDER BY o.outfit_id) as outfit_names,
                    array_agg(o.outfit_type ORDER BY o.outfit_id) as outfit_types,
                    array_agg(o.outfit_color ORDER BY o.outfit_id) as outfit_colors,
                    array_agg(o.outfit_desc ORDER BY o.outfit_id) as outfit_descriptions,
                    array_agg(o.rent_price ORDER BY o.outfit_id) as outfit_prices,
                    array_agg(o.outfit_img ORDER BY o.outfit_id) as outfit_images
                FROM gown_package_outfits gpo
                JOIN outfits o ON gpo.outfit_id = o.outfit_id
                GROUP BY gpo.gown_package_id
            )
            SELECT 
                e.events_id, e.event_name, e.event_type, e.event_theme, e.event_color, 
                e.schedule, e.start_time, e.end_time, e.status,
                ep.package_id, ep.package_name, ep.capacity, 
                ep.description AS package_description, ep.total_price,
                v.venue_name, v.location, 
                gp.gown_package_name, gp.gown_package_price,
                od.outfit_ids,
                od.outfit_names,
                od.outfit_types,
                od.outfit_colors,
                od.outfit_descriptions,
                od.outfit_prices,
                od.outfit_images,
                array_remove(array_agg(DISTINCT CASE WHEN ps.supplier_id IS NOT NULL THEN ps.package_service_id END), NULL) AS internal_package_service_ids,
                array_remove(array_agg(DISTINCT CASE WHEN ps.supplier_id IS NOT NULL THEN ps.supplier_id END), NULL) AS internal_supplier_ids,
                array_remove(array_agg(DISTINCT CASE WHEN ps.supplier_id IS NOT NULL THEN u.firstname || ' ' || u.lastname END), NULL) AS internal_supplier_names,
                array_remove(array_agg(DISTINCT CASE WHEN ps.supplier_id IS NOT NULL THEN s.service END), NULL) AS internal_services,
                array_remove(array_agg(DISTINCT CASE WHEN ps.supplier_id IS NOT NULL THEN s.price END), NULL) AS internal_service_prices,
                array_remove(array_agg(DISTINCT CASE WHEN ps.supplier_id IS NULL THEN ps.package_service_id END), NULL) AS external_package_service_ids,
                array_remove(array_agg(DISTINCT CASE WHEN ps.supplier_id IS NULL THEN ps.external_supplier_name END), NULL) AS external_supplier_names,
                array_remove(array_agg(DISTINCT CASE WHEN ps.supplier_id IS NULL THEN ps.external_supplier_contact END), NULL) AS external_supplier_contacts,
                array_remove(array_agg(DISTINCT CASE WHEN ps.supplier_id IS NULL THEN ps.external_supplier_price END), NULL) AS external_supplier_prices,
                array_remove(array_agg(DISTINCT ads.add_service_id), NULL) AS additional_service_ids,
                array_remove(array_agg(DISTINCT ads.add_service_name), NULL) AS additional_service_names,
                array_remove(array_agg(DISTINCT ads.add_service_description), NULL) AS additional_service_descriptions,
                array_remove(array_agg(DISTINCT ads.add_service_price), NULL) AS additional_service_prices
            FROM events e
            LEFT JOIN event_packages ep ON e.package_id = ep.package_id
            LEFT JOIN venues v ON ep.venue_id = v.venue_id
            LEFT JOIN gown_package gp ON ep.gown_package_id = gp.gown_package_id
            LEFT JOIN outfit_details od ON gp.gown_package_id = od.gown_package_id
            LEFT JOIN event_package_services eps ON ep.package_id = eps.package_id
            LEFT JOIN package_service ps ON eps.package_service_id = ps.package_service_id
            LEFT JOIN suppliers s ON ps.supplier_id = s.supplier_id
            LEFT JOIN users u ON s.userid = u.userid
            LEFT JOIN event_package_additional_services epas ON ep.package_id = epas.package_id
            LEFT JOIN additional_services ads ON epas.add_service_id = ads.add_service_id
            WHERE e.userid = %s
            GROUP BY 
                e.events_id, ep.package_id, v.venue_name, v.location, 
                gp.gown_package_name, gp.gown_package_price,
                od.outfit_ids, od.outfit_names, od.outfit_types, 
                od.outfit_colors, od.outfit_descriptions, od.outfit_prices, od.outfit_images
        """, (userid,))
        columns = [desc[0] for desc in cursor.description]
        wishlist = cursor.fetchall()

        # Convert the result to dictionaries and ensure time objects are strings
        result = []
        for item in wishlist:
            item_dict = dict(zip(columns, item))
            
            # Format time objects
            if isinstance(item_dict['start_time'], time):
                item_dict['start_time'] = item_dict['start_time'].strftime("%H:%M:%S")
            if isinstance(item_dict['end_time'], time):
                item_dict['end_time'] = item_dict['end_time'].strftime("%H:%M:%S")
            
            # Format outfit details
            if item_dict.get('outfit_ids'):
                item_dict['outfits'] = [
                    {
                        'outfit_id': outfit_id,
                        'outfit_name': name,
                        'outfit_type': type_,
                        'outfit_color': color,
                        'outfit_desc': desc,
                        'rent_price': price,
                        'outfit_img': img
                    }
                    for outfit_id, name, type_, color, desc, price, img in zip(
                        item_dict['outfit_ids'],
                        item_dict['outfit_names'],
                        item_dict['outfit_types'],
                        item_dict['outfit_colors'],
                        item_dict['outfit_descriptions'],
                        item_dict['outfit_prices'],
                        item_dict['outfit_images']
                    )
                ]
            else:
                item_dict['outfits'] = []

            # Clean up outfit temporary fields
            del item_dict['outfit_ids']
            del item_dict['outfit_names']
            del item_dict['outfit_types']
            del item_dict['outfit_colors']
            del item_dict['outfit_descriptions']
            del item_dict['outfit_prices']
            del item_dict['outfit_images']
            
            # Format additional services
            if item_dict['additional_service_ids']:
                item_dict['additional_services'] = [
                    {
                        'add_service_id': service_id,
                        'add_service_name': name,
                        'add_service_description': description,
                        'add_service_price': price
                    }
                    for service_id, name, description, price in zip(
                        item_dict['additional_service_ids'],
                        item_dict['additional_service_names'],
                        item_dict['additional_service_descriptions'],
                        item_dict['additional_service_prices']
                    )
                ]
            else:
                item_dict['additional_services'] = []

            # Clean up additional services temporary fields
            del item_dict['additional_service_ids']
            del item_dict['additional_service_names']
            del item_dict['additional_service_descriptions']
            del item_dict['additional_service_prices']

            result.append(item_dict)

        return result

    except Exception as e:
        print(f"Error in get_user_wishlist: {str(e)}")
        raise e
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
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        logger.error(f"Error getting user ID by email: {str(e)}")
        raise
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
    conn = get_db_connection()  # Assuming you have a function to get the DB connection
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
        # Get basic package information with event type
        cursor.execute("""
            SELECT 
                p.package_id,
                p.package_name,
                et.event_type_name,
                p.event_type_id,
                p.capacity,
                p.description,
                p.venue_id,
                v.venue_name,
                p.gown_package_id,
                gp.gown_package_name,
                p.additional_capacity_charges,
                p.charge_unit,
                p.total_price,
                p.created_at,
                p.status
            FROM event_packages p
            LEFT JOIN venues v ON p.venue_id = v.venue_id
            LEFT JOIN gown_package gp ON p.gown_package_id = gp.gown_package_id
            LEFT JOIN event_type et ON p.event_type_id = et.event_type_id
            ORDER BY p.created_at DESC
        """)
        rows = cursor.fetchall()
        
        # Convert rows to dictionaries
        packages = []
        for row in rows:
            package = {
                'package_id': row[0],
                'package_name': row[1],
                'event_type_name': row[2],
                'event_type_id': row[3],
                'capacity': row[4],
                'description': row[5],
                'venue_id': row[6],
                'venue_name': row[7],
                'gown_package_id': row[8],
                'gown_package_name': row[9],
                'additional_capacity_charges': float(row[10]) if row[10] else 0,
                'charge_unit': row[11],
                'total_price': float(row[12]) if row[12] else 0,
                'created_at': row[13].strftime('%Y-%m-%d') if row[13] else None,
                'status': row[14]
            }
            
            # Get suppliers for this package
            cursor.execute("""
                SELECT 
                    s.supplier_id,
                    u.firstname,
                    u.lastname,
                    s.service,
                    s.price,
                    ps.remarks
                FROM event_package_services eps
                JOIN package_service ps ON eps.package_service_id = ps.package_service_id
                JOIN suppliers s ON ps.supplier_id = s.supplier_id
                JOIN users u ON s.userid = u.userid
                WHERE eps.package_id = %s
            """, (row[0],))  # Use row[0] for package_id
            
            package['suppliers'] = []
            supplier_rows = cursor.fetchall()
            for supplier_row in supplier_rows:
                package['suppliers'].append({
                    'supplier_id': supplier_row[0],
                    'name': f"{supplier_row[1]} {supplier_row[2]}",
                    'service': supplier_row[3],
                    'price': float(supplier_row[4]) if supplier_row[4] else 0,
                    'remarks': supplier_row[5]
                })
                
            # Get additional services for this package
            cursor.execute("""
                SELECT 
                    a.add_service_id,
                    a.add_service_name,
                    a.add_service_price
                FROM event_package_additional_services epas
                JOIN additional_services a ON epas.add_service_id = a.add_service_id
                WHERE epas.package_id = %s
            """, (row[0],))  # Use row[0] for package_id
            
            package['additional_services'] = []
            service_rows = cursor.fetchall()
            for service_row in service_rows:
                package['additional_services'].append({
                    'service_id': service_row[0],
                    'name': service_row[1],
                    'price': float(service_row[2]) if service_row[2] else 0
                })
            
            packages.append(package)
        
        return packages
    except Exception as e:
        print(f"Error fetching packages: {e}")
        raise e
    finally:
        cursor.close()
        conn.close()



def get_package_details_by_id(package_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT ep.package_id, ep.package_name, et.event_type_name, ep.capacity, ep.description, ep.total_price,
                   ep.additional_capacity_charges, ep.charge_unit,
                   v.venue_name, v.location, v.venue_price,
                   gp.gown_package_name, gp.gown_package_price,
                   array_agg(ps.package_service_id) AS package_service_ids,
                   array_agg(ps.supplier_id) AS supplier_ids,
                   array_agg(s.service) AS services,
                   array_agg(s.price) AS service_prices,
                   array_agg(u.firstname) AS supplier_firstnames,
                   array_agg(u.lastname) AS supplier_lastnames,
                   array_agg(u.email) AS supplier_emails,
                   array_agg(ps.external_supplier_name) AS external_supplier_names,
                   array_agg(ps.external_supplier_contact) AS external_supplier_contacts,
                   array_agg(ps.external_supplier_price) AS external_supplier_prices,
                   array_agg(ps.remarks) AS remarks
            FROM event_packages ep
            LEFT JOIN event_type et ON ep.event_type_id = et.event_type_id
            LEFT JOIN venues v ON ep.venue_id = v.venue_id
            LEFT JOIN gown_package gp ON ep.gown_package_id = gp.gown_package_id
            LEFT JOIN event_package_services eps ON ep.package_id = eps.package_id
            LEFT JOIN package_service ps ON eps.package_service_id = ps.package_service_id
            LEFT JOIN suppliers s ON ps.supplier_id = s.supplier_id
            LEFT JOIN users u ON s.userid = u.userid
            WHERE ep.package_id = %s
            GROUP BY ep.package_id, et.event_type_name, v.venue_name, v.location, v.venue_price, 
                     gp.gown_package_name, gp.gown_package_price
        """, (package_id,))
        
        row = cursor.fetchone()
        if row:
            return {
                'package_id': row[0],
                'package_name': row[1],
                'event_type_name': row[2],
                'capacity': row[3],
                'description': row[4],
                'total_price': float(row[5]) if row[5] else 0,
                'additional_capacity_charges': float(row[6]) if row[6] else 0,
                'charge_unit': row[7],
                'venue_name': row[8],
                'venue_location': row[9],
                'venue_price': float(row[10]) if row[10] else 0,
                'gown_package_name': row[11],
                'gown_package_price': float(row[12]) if row[12] else 0,
                'package_service_ids': row[13] if row[13] and row[13][0] is not None else [],
                'supplier_ids': row[14] if row[14] and row[14][0] is not None else [],
                'services': row[15] if row[15] and row[15][0] is not None else [],
                'service_prices': [float(p) if p else 0 for p in row[16]] if row[16] and row[16][0] is not None else [],
                'supplier_firstnames': row[17] if row[17] and row[17][0] is not None else [],
                'supplier_lastnames': row[18] if row[18] and row[18][0] is not None else [],
                'supplier_emails': row[19] if row[19] and row[19][0] is not None else [],
                'external_supplier_names': row[20] if row[20] and row[20][0] is not None else [],
                'external_supplier_contacts': row[21] if row[21] and row[21][0] is not None else [],
                'external_supplier_prices': [float(p) if p else 0 for p in row[22]] if row[22] and row[22][0] is not None else [],
                'remarks': row[23] if row[23] and row[23][0] is not None else []
            }
        return None
    finally:
        cursor.close()
        conn.close()



def add_to_wishlist(userid, event_data):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Start a transaction
        cursor.execute("BEGIN")
        
        # Insert into events table
        cursor.execute("""
            INSERT INTO events (
                userid, event_name, event_type, event_theme, event_color,
                package_id, schedule, start_time, end_time, status
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, 'Wishlist'
            ) RETURNING events_id
        """, (
            userid, event_data['event_name'], event_data['event_type'],
            event_data['event_theme'], event_data['event_color'],
            event_data['package_id'], event_data['schedule'], 
            event_data['start_time'], event_data['end_time']
        ))
        
        events_id = cursor.fetchone()[0]

        # Process suppliers
        for supplier in event_data.get('suppliers', []):
            if not supplier.get('is_removed'):  # Don't add removed suppliers
                cursor.execute("""
                    INSERT INTO event_suppliers (
                        events_id, supplier_id, is_modified,
                        modified_price, external_supplier_name, 
                        external_supplier_contact, external_supplier_price
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    events_id,
                    supplier.get('supplier_id'),
                    supplier.get('is_modified', False) or supplier.get('is_added', False),
                    supplier.get('price'),
                    supplier.get('external_supplier_name'),
                    supplier.get('external_supplier_contact'),
                    supplier.get('external_supplier_price')
                ))

        # Process venues
        for venue in event_data.get('venues', []):
            if not venue.get('is_removed'):  # Don't add removed venues
                cursor.execute("""
                    INSERT INTO event_venues (
                        events_id, venue_id, is_modified,
                        modified_price
                    )
                    VALUES (%s, %s, %s, %s)
                """, (
                    events_id,
                    venue['venue_id'],
                    venue.get('is_modified', False) or venue.get('is_added', False),
                    venue.get('price')
                ))

        cursor.execute("COMMIT")
        return events_id

    except Exception as e:
        cursor.execute("ROLLBACK")
        logger.error(f"Error in add_to_wishlist: {str(e)}")
        raise
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


# Function to fetch all additional services from the additional_services table
def get_all_additional_services():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT add_service_id, add_service_name, add_service_description, add_service_price FROM additional_services")
        services = cursor.fetchall()

        # Transform the result into a list of dictionaries
        return [
            {
                'add_service_id': item[0],
                'add_service_name': item[1],
                'add_service_description': item[2],
                'add_service_price': item[3]
            }
            for item in services
        ]
    finally:
        cursor.close()
        conn.close()




def get_event_types():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT event_type_id, event_type_name 
            FROM event_type 
            ORDER BY event_type_name
        """)
        rows = cursor.fetchall()
        event_types = [
            {
                'event_type_id': row[0],
                'event_type_name': row[1]
            }
            for row in rows
        ]
        return event_types
    except Exception as e:
        print(f"Error fetching event types: {e}")
        raise e
    finally:
        cursor.close()
        conn.close()

def initialize_event_types():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # First check if we already have event types
        cursor.execute("SELECT COUNT(*) FROM event_type")
        count = cursor.fetchone()[0]
        logging.info(f"Current event type count: {count}")
        
        if count == 0:
            # Insert default event types
            event_types = [
                'Wedding',
                'Birthday',
                'Corporate Event',
                'Anniversary',
                'Graduation',
                'Family Gathering',
                'Reunion',
                'Conference',
                'Seminar',
                'Other'
            ]
            
            for event_type in event_types:
                logging.info(f"Inserting event type: {event_type}")
                cursor.execute(
                    "INSERT INTO event_type (event_type_name) VALUES (%s)",
                    (event_type,)
                )
            
            conn.commit()
            logging.info("Default event types initialized successfully")
        else:
            logging.info("Event types already exist, skipping initialization")
        
    except Exception as e:
        conn.rollback()
        logging.error(f"Error initializing event types: {e}")
        raise e
    finally:
        cursor.close()
        conn.close()

def get_booked_schedules():
    """
    Get all booked event schedules that are not cancelled
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        query = """
            SELECT schedule, start_time, end_time 
            FROM events 
            WHERE schedule IS NOT NULL 
            AND start_time IS NOT NULL 
            AND end_time IS NOT NULL 
            AND schedule >= CURRENT_DATE 
            AND (status = 'Wishlist' OR status IS NULL)
            ORDER BY schedule, start_time
        """
        
        cursor.execute(query)
        schedules = cursor.fetchall()
        
        if schedules:
            return [
                {
                    'schedule': schedule.strftime('%Y-%m-%d') if schedule else None,
                    'start_time': start_time.strftime('%H:%M') if start_time else None,
                    'end_time': end_time.strftime('%H:%M') if end_time else None
                }
                for schedule, start_time, end_time in schedules
            ]
        return []
        
    except Exception as e:
        logger.error(f"Error fetching booked schedules: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


def track_service_modification(events_id, package_service_id, modification_type, original_price=None, modified_price=None, remarks=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO modified_event_services 
            (event_id, package_service_id, modification_type, original_price, modified_price, remarks)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING modification_id
        """, (events_id, package_service_id, modification_type, original_price, modified_price, remarks))
        
        modification_id = cursor.fetchone()[0]
        conn.commit()
        return modification_id
    except Exception as e:
        conn.rollback()
        logger.error(f"Error tracking service modification: {str(e)}")
        raise
    finally:
        cursor.close()
        conn.close()

def add_service_customization(events_id, package_service_id, custom_price=None, custom_details=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO event_service_customizations 
            (event_id, package_service_id, custom_price, custom_details)
            VALUES (%s, %s, %s, %s)
            RETURNING customization_id
        """, (events_id, package_service_id, custom_price, custom_details))
        
        customization_id = cursor.fetchone()[0]
        conn.commit()
        return customization_id
    except Exception as e:
        conn.rollback()
        logger.error(f"Error adding service customization: {str(e)}")
        raise
    finally:
        cursor.close()
        conn.close()

def get_event_modifications(events_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Get all modifications for the event
        cursor.execute("""
            SELECT m.modification_id, m.package_service_id, m.modification_type,
                   m.original_price, m.modified_price, m.remarks,
                   COALESCE(ps.supplier_id::text, ps.external_supplier_name) as supplier_identifier,
                   ps.external_supplier_contact, ps.external_supplier_price
            FROM modified_event_services m
            JOIN package_service ps ON m.package_service_id = ps.package_service_id
            WHERE m.event_id = %s
            ORDER BY m.created_at
        """, (events_id,))
        
        modifications = cursor.fetchall()
        
        # Get all customizations for the event
        cursor.execute("""
            SELECT c.customization_id, c.package_service_id, c.custom_price,
                   c.custom_details,
                   COALESCE(ps.supplier_id::text, ps.external_supplier_name) as supplier_identifier
            FROM event_service_customizations c
            JOIN package_service ps ON c.package_service_id = ps.package_service_id
            WHERE c.event_id = %s
            ORDER BY c.created_at
        """, (events_id,))
        
        customizations = cursor.fetchall()
        
        return {
            'modifications': [{
                'modification_id': m[0],
                'package_service_id': m[1],
                'modification_type': m[2],
                'original_price': float(m[3]) if m[3] else None,
                'modified_price': float(m[4]) if m[4] else None,
                'remarks': m[5],
                'supplier_identifier': m[6],
                'external_supplier_contact': m[7],
                'external_supplier_price': float(m[8]) if m[8] else None
            } for m in modifications],
            'customizations': [{
                'customization_id': c[0],
                'package_service_id': c[1],
                'custom_price': float(c[2]) if c[2] else None,
                'custom_details': c[3],
                'supplier_identifier': c[4]
            } for c in customizations]
        }
    finally:
        cursor.close()
        conn.close()
