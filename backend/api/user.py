import logging
from mysql.connector import Error
from typing import Optional

# Import the database connection and security functions
from database.connection import get_db_connection
from core.security import hash_password, verify_password

# Configure logging for this module
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Member:
    """
    Represents a gym member and handles all related database operations
    such as registration, authentication, and data management (CRUD).
    """

    def __init__(self, member_ID, name, email, password, status, phone_number=None, membership_plan=None, join_date=None):
        """Initializes a Member object with data for an existing member."""
        self.member_ID = member_ID
        self.name = name
        self.email = email
        self.password = password
        self.status = status
        self.phone_number = phone_number
        self.membership_plan = membership_plan
        self.join_date = join_date

    # --- Authentication and Creation Methods ---

    @staticmethod
    def email_exists(email: str) -> bool:
        """Checks if a member with the given email already exists."""
        query = "SELECT email FROM Members WHERE email = %s"
        try:
            conn = get_db_connection()
            if conn is None:
                logging.error("Failed to establish database connection.")
                return True # Fail safely
            with conn.cursor() as cursor:
                cursor.execute(query, (email,))
                return cursor.fetchone() is not None
        except Error as e:
            logging.error(f"Database error while checking if email exists: {e}")
            return True

    @classmethod
    def create(cls, name: str, email: str, password: str, phone_number: str, membership_plan: str, join_date: str) -> Optional['Member']:
        """Registers a new member by hashing their password and inserting them into the database."""
        if cls.email_exists(email):
            logging.warning(f"Registration attempt for already existing email: {email}")
            return None

        hashed_pw = hash_password(password)
        
        query = """
            INSERT INTO Members (name, email, password, phone_number, membership_plan, join_date)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        try:
            conn = get_db_connection()
            if conn is None:
                logging.error("Failed to establish database connection.")
                return None
            with conn.cursor() as cursor:
                cursor.execute(query, (name, email, hashed_pw, phone_number, membership_plan, join_date))
                conn.commit()
                member_ID = cursor.lastrowid
                logging.info(f"Successfully registered new member: {name} ({email}) with ID: {member_ID}")
                return cls(member_ID=member_ID, name=name, email=email, password=hashed_pw, status='active')
        except Error as e:
            logging.error(f"Failed to register member {name}: {e}")
            return None

    @classmethod
    def authenticate(cls, email: str, password: str) -> Optional['Member']:
        """Authenticates a member by verifying their email and password."""
        query = "SELECT member_ID, name, email, password, status FROM Members WHERE email = %s"
        
        try:
            conn = get_db_connection()
            if conn is None:
                logging.error("Failed to establish database connection.")
                return None
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(query, (email,))
                result = cursor.fetchone()
                
                if not result:
                    logging.warning(f"Login failed: No user found with email {email}")
                    return None
                    
                if verify_password(password, result['password']):
                    logging.info(f"Login successful for member: {result['name']} ({email})")
                    cls._log_activity(result['member_ID'], "Login Successful")
                    return cls(member_ID=result['member_ID'], name=result['name'], email=result['email'], password=result['password'], status=result['status'])
                else:
                    logging.warning(f"Login failed: Invalid password for {email}")
                    cls._log_activity(result['member_ID'], "Invalid Password")
                    return None
        except Error as e:
            logging.error(f"Database error during authentication for {email}: {e}")
            return None

    # --- NEW CRUD Methods ---

    @staticmethod
    def get_all() -> list['Member']:
        """Retrieves all members from the database."""
        query = "SELECT * FROM Members ORDER BY name ASC"
        members_list = []
        try:
            conn = get_db_connection()
            if conn is None:
                logging.error("Failed to establish database connection.")
                return []
            if conn is None:
                logging.error("Failed to establish database connection.")
                return []
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(query)
                res = cursor.fetchall()
                if res:
                    for row in res:
                        members_list.append(Member(**row))
        except Error as e:
            logging.error(f"Database error while fetching all members: {e}")
        return members_list

    @staticmethod
    def find_by_id(member_ID: int) -> Optional['Member']:
        """Finds a single member by their ID."""
        query = "SELECT * FROM Members WHERE member_ID = %s"
        try:
            conn = get_db_connection()
            if conn is None:
                logging.error("Failed to establish database connection.")
                return None
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(query, (member_ID,))
                result = cursor.fetchone()
                if result:
                    return Member(**result)
        except Error as e:
            logging.error(f"Database error finding member by ID {member_ID}: {e}")
        return None

    @staticmethod
    def update(member_ID: int, updates: dict) -> Optional['Member']:
        """Updates one or more fields for a member."""
        valid_columns = ['name', 'email', 'phone_number', 'membership_plan', 'status']
        
        set_clause_parts = [f"{key} = %s" for key in updates if key in valid_columns]
        if not set_clause_parts:
            logging.warning("Update called with no valid fields.")
            return None

        query = f"UPDATE Members SET {', '.join(set_clause_parts)} WHERE member_ID = %s"
        values = list(updates.values()) + [member_ID]

        try:
            conn = get_db_connection()
            if conn is None:
                logging.error("Failed to establish database connection.")
                return None
            with conn.cursor() as cursor:
                cursor.execute(query, tuple(values))
                conn.commit()
                if cursor.rowcount > 0:
                    return Member.find_by_id(member_ID)
        except Error as e:
            logging.error(f"Database error updating member {member_ID}: {e}")
        return None

    @staticmethod
    def delete(member_ID: int) -> bool:
        """Deletes a member from the database."""
        query = "DELETE FROM Members WHERE member_ID = %s"
        try:
            conn = get_db_connection()
            if conn is None:
                logging.error("Failed to establish database connection.")
                return False
            with conn.cursor() as cursor:
                cursor.execute(query, (member_ID,))
                conn.commit()
                return cursor.rowcount > 0
        except Error as e:
            logging.error(f"Database error deleting member {member_ID}: {e}")
        return False

    # --- Private Helper Methods ---
    
    @staticmethod
    def _log_activity(member_ID: int, status: str):
        """Private helper to log login attempts to the MLD table."""
        query = "INSERT INTO MLD (mem_id, login_status) VALUES (%s, %s)"
        try:
            conn = get_db_connection()
            if conn is None:
                logging.error("Failed to establish database connection.")
                return
            with conn.cursor() as cursor:
                cursor.execute(query, (member_ID, status))
                conn.commit()
        except Error as e:
            logging.error(f"Failed to log activity for member ID {member_ID}: {e}")
