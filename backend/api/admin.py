import logging
from mysql.connector import Error
from typing import Optional

# Import the database connection and security functions from your project
from database.connection import get_db_connection
from core.security import hash_password, verify_password

# Configure logging for the admin module
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Admin:
    """
    Represents a gym administrator and handles all related database operations,
    including registration, authentication, and logging activities.
    """

    def __init__(self, ad_ID, name, username):
        """Initializes an Admin object with data for an existing administrator."""
        self.ad_ID = ad_ID  # CORRECTED: Attribute now matches database column
        self.name = name
        self.username = username

    @staticmethod
    def username_exists(username: str) -> bool:
        """
        Checks if an admin with the given username already exists in the database.

        Args:
            username (str): The username to check.

        Returns:
            bool: True if the username exists, False otherwise.
        """
        query = "SELECT username FROM ADMIN WHERE username = %s"
        try:
            conn = get_db_connection()
            if conn is None:
                logging.error("Failed to establish database connection.")
                return False
            with conn.cursor() as cursor:
                cursor.execute(query, (username,))
                return cursor.fetchone() is not None
        except Error as e:
            logging.error(f"Database error while checking if admin username exists: {e}")
            # Prevent registration on database error for security
            return True

    @classmethod
    def create(cls, name: str, username: str, password: str) -> Optional['Admin']:
        """
        Registers a new administrator, securely hashing their password before storage.

        Args:
            name (str): The administrator's full name.
            username (str): The administrator's username for logging in.
            password (str): The administrator's plain-text password.

        Returns:
            A new Admin object if registration is successful, otherwise None.
        """
        if cls.username_exists(username):
            logging.warning(f"Registration attempt for already existing admin username: {username}")
            return None

        # Hash the password using the secure function from security.py
        hashed_pw = hash_password(password)
        
        query = "INSERT INTO ADMIN (name, username, password) VALUES (%s, %s, %s)"
        
        try:
            conn = get_db_connection()
            if conn is None:
                logging.error("Failed to establish database connection.")
                return None
            with conn.cursor() as cursor:
                cursor.execute(query, (name, username, hashed_pw))
                conn.commit()
                admin_id = cursor.lastrowid
                logging.info(f"Successfully registered new admin: {name} ({username}) with ID: {admin_id}")
                return cls(ad_ID=admin_id, name=name, username=username)
        except Error as e:
            logging.error(f"Failed to register admin {name}: {e}")
            return None

    @classmethod
    def authenticate(cls, username: str, password: str) -> Optional['Admin']:
        """
        Authenticates an administrator by verifying their username and password.

        Args:
            username (str): The admin's username.
            password (str): The plain-text password to verify.

        Returns:
            An Admin object if authentication is successful, otherwise None.
        """
        query = "SELECT ad_ID, name, username, password FROM ADMIN WHERE username = %s"
        
        try:
            conn = get_db_connection()
            if conn is None:
                logging.error("Failed to establish database connection.")
                return None
            with conn.cursor() as cursor:
                cursor.execute(query, (username,))
                result = cursor.fetchone()

                if not result:
                    logging.warning(f"Admin login failed: No admin found with username {username}")
                    return None
                    
                admin_id, name, db_username, hashed_password = result
                
                # Use the secure verify_password function
                if verify_password(password, hashed_password):
                    logging.info(f"Login successful for admin: {name} ({username})")
                    # Log the successful login attempt
                    cls._log_activity(admin_id, "Login Successful")
                    return cls(ad_ID=admin_id, name=name, username=db_username)
                else:
                    logging.warning(f"Admin login failed: Invalid password for {username}")
                    # Log the failed login attempt
                    cls._log_activity(admin_id, "Invalid Password")
                    return None
        except Error as e:
            logging.error(f"Database error during admin authentication for {username}: {e}")
            return None

    @staticmethod
    def _log_activity(admin_id: int, status: str):
        """
        Private helper method to log admin login attempts to the ALD table.

        Args:
            admin_id (int): The ID of the admin attempting to log in.
            status (str): The result of the login attempt (e.g., "Login Successful").
        """
        query = "INSERT INTO ALD (ad_id, login_status) VALUES (%s, %s)"
        try:
            conn = get_db_connection()
            if conn is None:
                logging.error("Failed to establish database connection.")
                return None
            with conn.cursor() as cursor:
                cursor.execute(query, (admin_id, status))
                conn.commit()
        except Error as e:
            logging.error(f"Failed to log activity for admin ID {admin_id}: {e}")

