import logging
from mysql.connector import Error
from typing import Optional

# Import the centralized database connection
from database.connection import get_db_connection

# Configure logging for the equipment module
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Equipment:
    """
    Represents a piece of gym equipment and handles all related database
    operations (CRUD - Create, Read, Update, Delete).
    """

    def __init__(self, e_code, e_name, e_qty, e_unit_price, e_category):
        """Initializes an Equipment object."""
        self.e_code = e_code
        self.e_name = e_name
        self.e_qty = e_qty
        self.e_unit_price = e_unit_price
        self.e_category = e_category

    @staticmethod
    def get_all() -> list['Equipment']:
        """Retrieves all equipment from the database."""
        equipment_list = []
        query = "SELECT * FROM Equipment ORDER BY e_name ASC"
        try:
            with get_db_connection() as conn:
                if conn is None:
                    logging.error("Failed to establish database connection.")
                    return []
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(query)
                    for row in cursor.fetchall():
                        equipment_list.append(Equipment(**row))
        except Error as e:
            logging.error(f"Database error fetching all equipment: {e}")
        return equipment_list

    @staticmethod
    def find_by_id(e_code: int) -> Optional['Equipment']:
        """Finds a single piece of equipment by its code."""
        query = "SELECT * FROM Equipment WHERE e_code = %s"
        try:
            with get_db_connection() as conn:
                if conn is None:
                    logging.error("Failed to establish database connection.")
                    return None
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(query, (e_code,))
                    result = cursor.fetchone()
                    if result:
                        return Equipment(**result)
        except Error as e:
            logging.error(f"Database error finding equipment by ID {e_code}: {e}")
        return None

    @staticmethod
    def create(e_name: str, e_qty: int, e_unit_price: int, e_category: str) -> Optional['Equipment']:
        """Adds a new piece of equipment to the database."""
        query = "INSERT INTO Equipment (e_name, e_qty, e_unit_price, e_category) VALUES (%s, %s, %s, %s)"
        try:
            with get_db_connection() as conn:
                if conn is None:
                    logging.error("Failed to establish database connection.")
                    return None
                with conn.cursor() as cursor:
                    cursor.execute(query, (e_name, e_qty, e_unit_price, e_category))
                    conn.commit()
                    new_id = cursor.lastrowid
                    return Equipment(new_id, e_name, e_qty, e_unit_price, e_category)
        except Error as e:
            logging.error(f"Database error while creating equipment: {e}")
        return None

    @staticmethod
    def update(e_code: int, updates: dict) -> Optional['Equipment']:
        """Updates one or more fields for a piece of equipment."""
        valid_columns = ['e_name', 'e_qty', 'e_unit_price', 'e_category']
        
        set_clause_parts = [f"{key} = %s" for key in updates if key in valid_columns]
        if not set_clause_parts:
            return None

        query = f"UPDATE Equipment SET {', '.join(set_clause_parts)} WHERE e_code = %s"
        values = list(updates.values()) + [e_code]

        try:
            with get_db_connection() as conn:
                if conn is None:
                    logging.error("Failed to establish database connection.")
                    return None
                with conn.cursor() as cursor:
                    cursor.execute(query, tuple(values))
                    conn.commit()
                    if cursor.rowcount > 0:
                        return Equipment.find_by_id(e_code)
        except Error as e:
            logging.error(f"Database error updating equipment {e_code}: {e}")
        return None

    @staticmethod
    def delete(e_code: int) -> bool:
        """Deletes a piece of equipment from the database."""
        query = "DELETE FROM Equipment WHERE e_code = %s"
        try:
            with get_db_connection() as conn:
                if conn is None:
                    logging.error("Failed to establish database connection.")
                    return False
                with conn.cursor() as cursor:
                    cursor.execute(query, (e_code,))
                    conn.commit()
                    return cursor.rowcount > 0
        except Error as e:
            logging.error(f"Database error deleting equipment {e_code}: {e}")
        return False
