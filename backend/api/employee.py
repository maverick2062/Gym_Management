import logging
from mysql.connector import Error
from typing import Optional

# Import the centralized database connection and security functions
from database.connection import get_db_connection
from core.security import hash_password, verify_password

# Configure logging for the employee module
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Employee:
    """
    Represents a gym employee and handles all related database operations,
    including registration, authentication, and activity logging.
    """

    def __init__(self, user_id, name, email, role, salary=0):
        """Initializes an Employee object with data for an existing employee."""
        self.user_id = user_id
        self.name = name
        self.email = email
        self.role = role
        self.salary = salary

    @staticmethod
    def email_exists(email: str) -> bool:
        """Checks if an employee with the given email already exists."""
        query = "SELECT email FROM Employee WHERE email = %s"
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (email,))
                    return cursor.fetchone() is not None
        except Error as e:
            logging.error(f"Database error while checking if employee email exists: {e}")
            return True

    @classmethod
    def create(cls, name: str, email: str, password: str, role: str, salary: int = 0) -> Optional['Employee']:
        """Registers a new employee, securely hashing their password."""
        if cls.email_exists(email):
            logging.warning(f"Registration attempt for existing employee email: {email}")
            return None

        hashed_pw = hash_password(password)
        query = "INSERT INTO Employee (name, email, password, role, salary) VALUES (%s, %s, %s, %s, %s)"
        
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (name, email, hashed_pw, role, salary))
                    conn.commit()
                    user_id = cursor.lastrowid
                    logging.info(f"Successfully registered new employee: {name} ({email}) with ID: {user_id}")
                    return cls(user_id=user_id, name=name, email=email, role=role, salary=salary)
        except Error as e:
            logging.error(f"Failed to register employee {name}: {e}")
            return None

    @classmethod
    def authenticate(cls, email: str, password: str) -> Optional['Employee']:
        """Authenticates an employee by verifying their email and password."""
        query = "SELECT user_id, name, email, password, role, salary FROM Employee WHERE email = %s"
        try:
            with get_db_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(query, (email,))
                    result = cursor.fetchone()
                    
                    if not result:
                        logging.warning(f"Employee login failed: No user found with email {email}")
                        return None
                        
                    if verify_password(password, result['password']):
                        logging.info(f"Login successful for employee: {result['name']} ({email})")
                        cls._log_activity(result['user_id'], "Login Successful")
                        # Unpack the full dictionary into the constructor
                        return cls(**result)
                    else:
                        logging.warning(f"Employee login failed: Invalid password for {email}")
                        cls._log_activity(result['user_id'], "Invalid Password")
                        return None
        except Error as e:
            logging.error(f"Database error during employee authentication for {email}: {e}")
            return None

    @staticmethod
    def get_all() -> list['Employee']:
        """Retrieves all employees from the database."""
        employees_list = []
        query = "SELECT user_id, name, email, role, salary FROM Employee ORDER BY name ASC"
        try:
            with get_db_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(query)
                    for row in cursor.fetchall():
                        employees_list.append(Employee(**row))
        except Error as e:
            logging.error(f"Database error fetching all employees: {e}")
        return employees_list

    @staticmethod
    def find_by_id(user_id: int) -> Optional['Employee']:
        """Finds a single employee by their user_id."""
        query = "SELECT user_id, name, email, role, salary FROM Employee WHERE user_id = %s"
        try:
            with get_db_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(query, (user_id,))
                    result = cursor.fetchone()
                    if result:
                        return Employee(**result)
        except Error as e:
            logging.error(f"Database error finding employee by ID {user_id}: {e}")
        return None

    @staticmethod
    def update(user_id: int, updates: dict) -> Optional['Employee']:
        """Updates fields for an employee."""
        valid_columns = ['name', 'email', 'role', 'salary']
        
        set_clause_parts = []
        values = []
        for key, value in updates.items():
            if key in valid_columns:
                set_clause_parts.append(f"{key} = %s")
                values.append(value)

        if not set_clause_parts:
            logging.warning("Update called with no valid columns to update.")
            return None

        query = f"UPDATE Employee SET {', '.join(set_clause_parts)} WHERE user_id = %s"
        values.append(user_id)

        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, tuple(values))
                    conn.commit()
                    if cursor.rowcount > 0:
                        return Employee.find_by_id(user_id)
                    else:
                        logging.warning(f"Update failed: No employee found with ID {user_id}")
                        return None
        except Error as e:
            logging.error(f"Database error updating employee {user_id}: {e}")
        return None

    @staticmethod
    def delete(user_id: int) -> bool:
        """Deletes an employee from the database."""
        query = "DELETE FROM Employee WHERE user_id = %s"
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (user_id,))
                    conn.commit()
                    return cursor.rowcount > 0
        except Error as e:
            logging.error(f"Database error deleting employee {user_id}: {e}")
        return False

    @staticmethod
    def _log_activity(employee_id: int, status: str):
        """Private helper to log employee login attempts."""
        query = "INSERT INTO ELD (emp_id, login_status) VALUES (%s, %s)"
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (employee_id, status))
                    conn.commit()
        except Error as e:
            logging.error(f"Failed to log activity for employee ID {employee_id}: {e}")
