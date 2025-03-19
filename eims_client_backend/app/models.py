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
                    wo.wishlist_id,
                    array_agg(
                        (o.outfit_id, o.outfit_name, o.outfit_type, o.outfit_color, o.outfit_desc, wo.price, o.outfit_img, wo.status, wo.remarks)::record
                        ORDER BY (o.outfit_id, o.outfit_name, o.outfit_type, o.outfit_color, o.outfit_desc, wo.price, o.outfit_img, wo.status, wo.remarks)
                    ) as outfit_details
                FROM wishlist_outfits wo
                JOIN outfits o ON wo.outfit_id = o.outfit_id
                GROUP BY wo.wishlist_id
            ),
            supplier_details AS (
                SELECT 
                    ws.wishlist_id,
                    array_agg(s.supplier_id ORDER BY s.supplier_id) as supplier_ids,
                    array_agg(u.firstname || ' ' || u.lastname ORDER BY s.supplier_id) as supplier_names,
                    array_agg(s.service ORDER BY s.supplier_id) as services,
                    array_agg(ws.price ORDER BY s.supplier_id) as prices,
                    array_agg(ws.status ORDER BY s.supplier_id) as statuses,
                    array_agg(ws.remarks ORDER BY s.supplier_id) as remarks
                FROM wishlist_suppliers ws
                JOIN suppliers s ON ws.supplier_id = s.supplier_id
                JOIN users u ON s.userid = u.userid
                GROUP BY ws.wishlist_id
            ),
            additional_service_details AS (
                SELECT 
                    was.wishlist_id,
                    array_agg(ads.add_service_id ORDER BY ads.add_service_id) as service_ids,
                    array_agg(ads.add_service_name ORDER BY ads.add_service_id) as service_names,
                    array_agg(ads.add_service_description ORDER BY ads.add_service_id) as service_descriptions,
                    array_agg(was.price ORDER BY ads.add_service_id) as service_prices,
                    array_agg(was.status ORDER BY ads.add_service_id) as service_statuses,
                    array_agg(was.remarks ORDER BY ads.add_service_id) as service_remarks
                FROM wishlist_additional_services was
                JOIN additional_services ads ON was.add_service_id = ads.add_service_id
                GROUP BY was.wishlist_id
            )
            SELECT 
                e.events_id, e.event_name, e.event_type, e.event_theme, e.event_color, 
                e.schedule, e.start_time, e.end_time, e.status as event_status,
                wp.wishlist_id, wp.package_name, wp.capacity, wp.description as package_description,
                wp.total_price, wp.additional_capacity_charges, wp.charge_unit, wp.status as package_status,
                v.venue_name, v.location, v.venue_price,
                gp.gown_package_name, gp.gown_package_price,
                od.outfit_details,
                sd.supplier_ids, sd.supplier_names, sd.services, sd.prices as supplier_prices,
                sd.statuses as supplier_statuses, sd.remarks as supplier_remarks,
                asd.service_ids, asd.service_names, asd.service_descriptions,
                asd.service_prices, asd.service_statuses, asd.service_remarks
            FROM events e
            JOIN wishlist_packages wp ON e.events_id = wp.events_id
            LEFT JOIN venues v ON wp.venue_id = v.venue_id
            LEFT JOIN gown_package gp ON wp.gown_package_id = gp.gown_package_id
            LEFT JOIN outfit_details od ON wp.wishlist_id = od.wishlist_id
            LEFT JOIN supplier_details sd ON wp.wishlist_id = sd.wishlist_id
            LEFT JOIN additional_service_details asd ON wp.wishlist_id = asd.wishlist_id
            WHERE e.userid = %s AND wp.status != 'Cancelled'
            ORDER BY wp.created_at DESC
        """, (userid,))

        columns = [desc[0] for desc in cursor.description]
        wishlist = cursor.fetchall()

        result = []
        for item in wishlist:
            item_dict = dict(zip(columns, item))
            
            # Format time objects
            if isinstance(item_dict['start_time'], time):
                item_dict['start_time'] = item_dict['start_time'].strftime("%H:%M:%S")
            if isinstance(item_dict['end_time'], time):
                item_dict['end_time'] = item_dict['end_time'].strftime("%H:%M:%S")
            
            # Format outfit details
            if item_dict.get('outfit_details'):
                logger.info(f"Processing outfits for wishlist. Raw outfit data: {item_dict}")
                item_dict['outfits'] = [
                    {
                        'outfit_id': details[0],
                        'outfit_name': details[1],
                        'outfit_type': details[2],
                        'outfit_color': details[3],
                        'outfit_desc': details[4],
                        'rent_price': details[5],
                        'outfit_img': details[6],
                        'status': details[7],
                        'remarks': details[8]
                    }
                    for details in item_dict['outfit_details']
                ]
                logger.info(f"Processed outfits: {item_dict['outfits']}")
            else:
                logger.info("No outfit_details found in item_dict")
                item_dict['outfits'] = []

            # Format supplier details
            if item_dict.get('supplier_ids'):
                item_dict['suppliers'] = [
                    {
                        'supplier_id': supplier_id,
                        'name': name,
                        'service': service,
                        'price': price,
                        'status': status,
                        'remarks': remarks
                    }
                    for supplier_id, name, service, price, status, remarks in zip(
                        item_dict['supplier_ids'],
                        item_dict['supplier_names'],
                        item_dict['services'],
                        item_dict['supplier_prices'],
                        item_dict['supplier_statuses'],
                        item_dict['supplier_remarks']
                    )
                ]
            else:
                item_dict['suppliers'] = []

            # Format additional services
            if item_dict.get('service_ids'):
                item_dict['additional_services'] = [
                    {
                        'add_service_id': service_id,
                        'add_service_name': name,
                        'add_service_description': description,
                        'add_service_price': price,
                        'status': status,
                        'remarks': remarks
                    }
                    for service_id, name, description, price, status, remarks in zip(
                        item_dict['service_ids'],
                        item_dict['service_names'],
                        item_dict['service_descriptions'],
                        item_dict['service_prices'],
                        item_dict['service_statuses'],
                        item_dict['service_remarks']
                    )
                ]
            else:
                item_dict['additional_services'] = []

            # Clean up temporary fields
            fields_to_remove = [
                'outfit_details',
                'supplier_ids', 'supplier_names', 'services', 'supplier_prices',
                'supplier_statuses', 'supplier_remarks',
                'service_ids', 'service_names', 'service_descriptions',
                'service_prices', 'service_statuses', 'service_remarks'
            ]
            for field in fields_to_remove:
                item_dict.pop(field, None)

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



def add_event_item(userid, event_name, event_type, event_theme, event_color, 
                  package_id, suppliers, schedule=None, start_time=None, 
                  end_time=None, status='Wishlist', total_price=0, outfits=None, 
                  services=None, additional_items=None, booking_type='Online'):
    """Add a new event with its package configuration"""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("BEGIN")

        # Ensure numeric values are properly formatted
        total_price = float(total_price) if total_price is not None else 0

        # Insert into events table
        cursor.execute("""
            INSERT INTO events (
                userid, event_name, event_type, event_theme, event_color, 
                package_id, schedule, start_time, end_time, status,
                total_price, booking_type
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
            RETURNING events_id
        """, (
            userid, event_name, event_type, event_theme, event_color, 
            package_id, schedule, start_time, end_time, status,
            total_price, booking_type
        ))
        events_id = cursor.fetchone()[0]

        # Create package configuration if package_id is provided
        if package_id:
            cursor.execute("""
                INSERT INTO event_package_configurations (events_id, package_id)
                VALUES (%s, %s)
                RETURNING config_id
            """, (events_id, package_id))
            config_id = cursor.fetchone()[0]

            # Store package suppliers
            if suppliers:
                for supplier in suppliers:
                    if not supplier:  # Skip if supplier is None
                        continue
                    cursor.execute("""
                        INSERT INTO event_package_suppliers (
                            config_id, supplier_id, original_price, modified_price,
                            is_modified, is_removed, remarks
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (
                        config_id,
                        supplier.get('supplier_id'),
                        float(supplier.get('original_price', 0) or 0),
                        float(supplier.get('modified_price', 0) or 0),
                        supplier.get('is_modified', False),
                        supplier.get('is_removed', False),
                        supplier.get('remarks', '')
                    ))

            # Store package outfits
            if outfits:
                for outfit in outfits:
                    if not outfit:  # Skip if outfit is None
                        continue
                    cursor.execute("""
                        INSERT INTO event_package_outfits (
                            config_id, outfit_id, gown_package_id,
                            original_price, modified_price,
                            is_modified, is_removed, remarks
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        config_id,
                        outfit.get('outfit_id'),
                        outfit.get('gown_package_id'),
                        float(outfit.get('original_price', 0) or 0),
                        float(outfit.get('modified_price', 0) or 0),
                        outfit.get('is_modified', False),
                        outfit.get('is_removed', False),
                        outfit.get('remarks', '')
                    ))

            # Store package services
            if services:
                for service in services:
                    if not service:  # Skip if service is None
                        continue
                    if 'package_service_id' in service:
                        cursor.execute("""
                            INSERT INTO event_package_services (package_id, package_service_id)
                            VALUES (%s, %s)
                        """, (
                            package_id,
                            service.get('package_service_id')
                        ))
                    else:
                        cursor.execute("""
                            INSERT INTO package_service (supplier_id, remarks)
                            VALUES (%s, %s)
                            RETURNING package_service_id
                        """, (
                            service.get('supplier_id'),
                            service.get('remarks', '')
                        ))
                        package_service_id = cursor.fetchone()[0]
                        cursor.execute("""
                            INSERT INTO event_package_services (package_id, package_service_id)
                            VALUES (%s, %s)
                        """, (
                            package_id,
                            package_service_id
                        ))

        # Store additional (non-package) items
        if additional_items:
            for item in additional_items:
                if not item:  # Skip if item is None
                    continue
                cursor.execute("""
                    INSERT INTO event_additional_items (
                        events_id, item_type, item_id, price, remarks
                    )
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    events_id,
                    item.get('item_type'),
                    item.get('item_id'),
                    float(item.get('price', 0) or 0),
                    item.get('remarks', '')
                ))

        cursor.execute("COMMIT")
        return events_id

    except Exception as e:
        cursor.execute("ROLLBACK")
        print(f"Error in add_event_item: {str(e)}")  # Add debug print
        raise e
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
        query = """
            WITH supplier_socials AS (
                SELECT 
                    supplier_id,
                    json_agg(
                        json_build_object(
                            'platform', platform,
                            'handle', handle,
                            'url', url
                        )
                    ) as social_media
                FROM supplier_social_media
                GROUP BY supplier_id
            )
            SELECT 
                s.supplier_id,
                s.service,
                s.price,
                s.status,
                u.userid,
                u.firstname,
                u.lastname,
                u.email,
                u.contactnumber,
                u.user_img,
                u.address,
                COALESCE(ss.social_media, '[]'::json) as social_media
            FROM suppliers s
            JOIN users u ON s.userid = u.userid
            LEFT JOIN supplier_socials ss ON s.supplier_id = ss.supplier_id
            ORDER BY s.supplier_id
        """
        
        # Debug logging
        logging.info("Executing supplier query...")
        cursor.execute(query)
        
        columns = [desc[0] for desc in cursor.description]
        suppliers = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        # Debug logging
        logging.info(f"Found {len(suppliers)} suppliers")
        if len(suppliers) == 0:
            logging.info("No suppliers found in the database")
        else:
            logging.info(f"First supplier: {suppliers[0]}")
        
        # Format the price to ensure it's a float
        for supplier in suppliers:
            supplier['price'] = float(supplier['price']) if supplier['price'] else 0.0
            
        return suppliers
    except Exception as e:
        logging.error(f"Error in get_available_suppliers: {e}")
        raise
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

def create_wishlist_package(events_id, package_data):
    """Create a new wishlist package for an event"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Insert the main wishlist package
        cursor.execute("""
            INSERT INTO wishlist_packages (
                events_id, package_name, capacity, description, venue_id,
                gown_package_id, additional_capacity_charges, charge_unit,
                total_price, event_type_id, status
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            ) RETURNING wishlist_id
        """, (
            events_id,
            package_data.get('package_name'),
            package_data.get('capacity'),
            package_data.get('description'),
            package_data.get('venue_id'),
            package_data.get('gown_package_id'),
            package_data.get('additional_capacity_charges', 0),
            package_data.get('charge_unit', 1),
            package_data.get('total_price', 0),
            package_data.get('event_type_id'),
            package_data.get('status', 'Active')
        ))
        
        wishlist_id = cursor.fetchone()[0]
        
        # Add services if provided
        if package_data.get('services'):
            for service in package_data['services']:
                cursor.execute("""
                    INSERT INTO wishlist_additional_services (wishlist_id, add_service_id, price, remarks)
                    VALUES (%s, %s, %s, %s)
                """, (
                    wishlist_id, 
                    service['add_service_id'],
                    service.get('price', 0),
                    service.get('remarks', '')
                ))
        
        # Add suppliers if provided
        if package_data.get('suppliers'):
            for supplier in package_data['suppliers']:
                cursor.execute("""
                    INSERT INTO wishlist_suppliers (wishlist_id, supplier_id, price, remarks)
                    VALUES (%s, %s, %s, %s)
                """, (
                    wishlist_id,
                    supplier['supplier_id'],
                    supplier.get('price'),
                    supplier.get('remarks')
                ))
        
        # Add outfits if provided
        if package_data.get('outfits'):
            for outfit in package_data['outfits']:
                cursor.execute("""
                    INSERT INTO wishlist_outfits (wishlist_id, outfit_id, gown_package_id, price, remarks)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    wishlist_id,
                    outfit.get('outfit_id'),
                    outfit.get('gown_package_id'),
                    outfit.get('price'),
                    outfit.get('remarks')
                ))
        
        conn.commit()
        return wishlist_id
        
    except Exception as e:
        conn.rollback()
        logger.error(f"Error creating wishlist package: {str(e)}")
        raise
    finally:
        cursor.close()
        conn.close()

def initialize_test_suppliers():
    """Initialize test suppliers for development purposes"""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # First, create test users
        test_users = [
            ('John', 'Doe', 'john.doe@test.com', '+1234567890', 'password123', 'Supplier', None, '123 Main St', 'johndoe'),
            ('Jane', 'Smith', 'jane.smith@test.com', '+1234567891', 'password123', 'Supplier', None, '456 Oak St', 'janesmith'),
            ('Mike', 'Johnson', 'mike.j@test.com', '+1234567892', 'password123', 'Supplier', None, '789 Pine St', 'mikej')
        ]

        for user in test_users:
            cursor.execute("""
                INSERT INTO users (firstname, lastname, email, contactnumber, password, user_type, user_img, address, username)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (email) DO NOTHING
                RETURNING userid
            """, user)
            
            userid = cursor.fetchone()
            if userid:
                # Add supplier entry
                cursor.execute("""
                    INSERT INTO suppliers (userid, service, price, status)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT DO NOTHING
                    RETURNING supplier_id
                """, (userid[0], f"Event Service by {user[0]}", 5000.00, 'active'))
                
                supplier_id = cursor.fetchone()
                if supplier_id:
                    # Add social media for the supplier
                    social_media = [
                        ('facebook', f'{user[8]}', f'https://facebook.com/{user[8]}'),
                        ('instagram', f'{user[8]}_events', f'https://instagram.com/{user[8]}_events'),
                    ]
                    
                    for platform, handle, url in social_media:
                        cursor.execute("""
                            INSERT INTO supplier_social_media (supplier_id, platform, handle, url)
                            VALUES (%s, %s, %s, %s)
                            ON CONFLICT DO NOTHING
                        """, (supplier_id[0], platform, handle, url))

        conn.commit()
        logging.info("Test suppliers initialized successfully")
        return True
    except Exception as e:
        conn.rollback()
        logging.error(f"Error initializing test suppliers: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def get_user_by_email(email):
    """
    Get user details by email.
    :param email: User's email address
    :return: User details as dictionary or None if not found
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            """SELECT userid, firstname, lastname, email, contactnumber, address, 
                     user_type, user_img, username
               FROM users 
               WHERE email = %s""", 
            (email,)
        )
        user = cursor.fetchone()
        
        if user:
            return {
                'userid': user[0],
                'firstname': user[1],
                'lastname': user[2],
                'email': user[3],
                'contactnumber': user[4],
                'address': user[5],
                'user_type': user[6],
                'user_img': user[7],
                'username': user[8]
            }
        return None
    except Exception as e:
        logger.error(f"Error getting user by email: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def update_user_profile(userid, firstname, lastname, username, contactnumber, address):
    """
    Update user profile information.
    :param userid: User ID
    :param firstname: First name
    :param lastname: Last name
    :param username: Username
    :param contactnumber: Contact number
    :param address: Address
    :return: True if successful, False otherwise
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            """UPDATE users 
               SET firstname = %s, lastname = %s, username = %s, contactnumber = %s, address = %s
               WHERE userid = %s""",
            (firstname, lastname, username, contactnumber, address, userid)
        )
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        logger.error(f"Error updating user profile: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

def update_user_profile_picture(userid, image_path):
    """
    Update user profile picture.
    :param userid: User ID
    :param image_path: Path to the uploaded image
    :return: True if successful, False otherwise
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Log the update attempt
        logger.info(f"Updating profile picture for user {userid} with path {image_path}")
        
        cursor.execute(
            """UPDATE users 
               SET user_img = %s
               WHERE userid = %s
               RETURNING user_img""",
            (image_path, userid)
        )
        
        # Get the updated value to confirm it worked
        updated_path = cursor.fetchone()
        
        conn.commit()
        
        if updated_path:
            logger.info(f"Successfully updated profile picture for user {userid}")
            return True
        
        logger.warning(f"Failed to update profile picture: no rows updated for user {userid}")
        return False
        
    except Exception as e:
        logger.error(f"Error updating user profile picture: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

def get_user_profile_by_id(userid):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT 
                userid,
                firstname,
                lastname,
                username,
                email,
                contactnumber,
                address,
                user_type,
                user_img
            FROM users 
            WHERE userid = %s
        """, (userid,))
        
        row = cursor.fetchone()
        
        if row:
            user_data = {
                'userid': row[0],
                'firstname': row[1],
                'lastname': row[2],
                'username': row[3],
                'email': row[4],
                'contactnumber': row[5],
                'address': row[6],
                'user_type': row[7].lower() if row[7] else None,
                'user_img': row[8]
            }
            
            logger.info(f"Raw user data from database: {user_data}")
            
            # If there's no profile picture, use the default
            if not user_data['user_img']:
                user_data['user_img'] = "/static/uploads/profile_pics/default-profile.jpg"
                logger.info("Using default profile picture")
            
            logger.info(f"Final user data: {user_data}")
            return user_data
            
        logger.warning(f"No user found with ID: {userid}")
        return None

    except Exception as e:
        logger.error(f"Error in get_user_profile_by_id: {e}")
        return None
    finally:
        cursor.close()
        conn.close()