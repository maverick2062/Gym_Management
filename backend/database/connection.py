import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_db_connection():
    """Establishes a connection to the MySQL database."""
    try:
        # It's better to connect directly to the database.
        # The database creation should be a one-time setup step.
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=os.getenv('MYSQL_PASSWORD'),
            database='GymDB' # Changed from Inventory to GymDB for clarity
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

def setup_database():
    """
    Sets up the database and tables.
    This should be run once manually or via a setup script.
    """
    try:
        # Connect without specifying a database to create it
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password=os.getenv('MYSQL_PASSWORD')
        )
        if conn is None:
            print("Failed to create database connection.")
            return
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS GymDB")
        print("Database 'GymDB' checked/created.")
        
        # User table (for both Admins and Employees, differentiated by a role)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(100) NOT NULL,
                role ENUM('admin', 'employee') NOT NULL,
                join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')

        # Members table (replaces Products)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Members (
                member_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                phone_number VARCHAR(20),
                membership_plan VARCHAR(50),
                join_date DATE NOT NULL,
                status ENUM('active', 'inactive', 'frozen') DEFAULT 'active'
            );
        ''')
        
        print("Tables 'Users' and 'Members' checked/created.")
        conn.commit()
        cursor.close()
        conn.close()
        print("Database setup complete.")

    except Error as e:
        print(f"Error during database setup: {e}")

if __name__ == '__main__':
    # This allows you to run `python connection.py` from the terminal to set up the DB
    print("Setting up the database...")
    setup_database()

