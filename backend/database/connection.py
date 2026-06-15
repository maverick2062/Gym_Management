import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
import logging

# Load environment variables from a .env file
load_dotenv()

# Configure logging to display info level messages
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_db_connection():
    """
    Establishes a connection to the MySQL database.
    Raises an exception if the connection fails.
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=os.getenv('MYSQL_PASSWORD'),
            database='GymDB',
            charset='utf8mb4'
        )
        if connection.is_connected():
            logging.info("Successfully connected to the GymDB database.")
            return connection
    except Error as e:
        logging.error(f"Error while connecting to MySQL: {e}")
        # Re-raise the exception to be handled by the caller
        raise

def setup_database():
    """
    Sets up the database and creates all necessary tables if they don't exist.
    This function is idempotent and can be run multiple times safely.
    """
    try:
        # Connect to MySQL server without specifying a database to create it
        with mysql.connector.connect(
            host='localhost',
            user='root',
            password=os.getenv('MYSQL_PASSWORD'),
            charset='utf8mb4'
        ) as conn:
            with conn.cursor() as cursor:
                # Create the database if it doesn't already exist
                cursor.execute("CREATE DATABASE IF NOT EXISTS GymDB")
                logging.info("Database 'GymDB' checked/created.")
                
                # Switch to the GymDB database for subsequent operations
                cursor.execute("USE GymDB")
                
                #-------------TABLES CREATION-----------------------------

                # Admin table to store administrator credentials
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS ADMIN(
                        ad_ID INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(50) NOT NULL,
                        username VARCHAR(50) UNIQUE NOT NULL,
                        password VARCHAR(255) NOT NULL
                    );
                ''')
                
                # Admin Login Details (ALD) table to log admin sign-ins
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS ALD(
                        login_id INT AUTO_INCREMENT PRIMARY KEY,
                        ad_id INT,
                        login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        user_status ENUM('active','deactivated') DEFAULT 'active',
                        login_status VARCHAR(50) NOT NULL DEFAULT 'Login Successful',
                        FOREIGN KEY (ad_id) REFERENCES ADMIN(ad_ID) ON DELETE CASCADE
                    );
                ''')

                # Employee table for staff like trainers and IT personnel
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Employee(
                        user_id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        email VARCHAR(100) UNIQUE NOT NULL,
                        password VARCHAR(255) NOT NULL,
                        salary INT,
                        role ENUM('IT', 'Trainer') NOT NULL,
                        join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                ''')

                # Employee Login Details (ELD) table to log employee sign-ins
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS ELD(
                        login_id INT AUTO_INCREMENT PRIMARY KEY,
                        emp_id INT,
                        login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        user_status ENUM('active','deactivated') DEFAULT 'active',
                        login_status VARCHAR(50) NOT NULL DEFAULT 'Login Successful',
                        FOREIGN KEY (emp_id) REFERENCES Employee(user_id) ON DELETE CASCADE
                    );
                ''')

                # Members table for gym clients
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Members(
                        member_ID INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        email VARCHAR(100) UNIQUE NOT NULL,
                        password VARCHAR(255) NOT NULL,
                        phone_number VARCHAR(20),
                        membership_plan VARCHAR(50),
                        join_date DATE NOT NULL,
                        status ENUM('active', 'inactive', 'frozen') DEFAULT 'active',
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                    );
                ''')

                # Member Login Details (MLD) table to log member sign-ins
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS MLD(
                        login_id INT AUTO_INCREMENT PRIMARY KEY,
                        mem_id INT,
                        login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        user_status ENUM('active','deactivated') DEFAULT 'active',
                        login_status VARCHAR(50) NOT NULL DEFAULT 'Login Successful',
                        FOREIGN KEY (mem_id) REFERENCES Members(member_ID) ON DELETE CASCADE
                    );
                ''')
                
                # Equipment table to track gym assets
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Equipment(
                        e_code INT AUTO_INCREMENT PRIMARY KEY,
                        e_name VARCHAR(50),
                        e_qty INT,
                        e_unit_price INT,
                        e_category VARCHAR(50)
                    );
                ''')

                cursor.execute('''
                    CREATE TABLE attendance (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        mem_id INT NOT NULL,
                        check_in DATETIME NOT NULL,
                        check_out DATETIME,                 
                        FOREIGN KEY (mem_id) REFERENCES Members(member_ID)
                    );
                ''')
                # check_out -- NULL until they leave

                cursor.execute('''
                    CREATE TABLE progress_logs (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        mem_id INT NOT NULL,
                        log_date DATE NOT NULL,
                        weight_kg DECIMAL(5,2),
                        body_fat_pct DECIMAL(4,2),
                        notes TEXT,
                        logged_by INT,                       
                        FOREIGN KEY (mem_id) REFERENCES members(member_ID)
                    );
                ''')
                # logged_by -- employee/trainer user_id
                
                #Payment/Revenue Logs
                cursor.execute('''
                    CREATE TABLE payments (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        mem_id INT NOT NULL,
                        amount DECIMAL(10,2) NOT NULL,
                        payment_date DATE NOT NULL,
                        payment_method VARCHAR(50),
                        plan_type VARCHAR(50),           
                        status ENUM('paid','pending','failed') DEFAULT 'paid',
                        FOREIGN KEY (mem_id) REFERENCES Members(member_ID)
                    );
                ''')
                # plan_type -- Monthly, Quarterly, Yearly


                # Member Reviews
                cursor.execute('''
                    CREATE TABLE reviews (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        member_id INT NOT NULL,
                        rating TINYINT CHECK (rating BETWEEN 1 AND 5),
                        review_text TEXT,
                        category VARCHAR(50),              
                        submitted_at DATETIME DEFAULT NOW(),
                        FOREIGN KEY (member_id) REFERENCES members(id)
                    );
                ''')
                # category -- Equipment, Trainer, Cleanliness etc.
                
                #Equipment Usage
                cursor.execute('''
                    CREATE TABLE equipment_usage (
                        id              INT AUTO_INCREMENT PRIMARY KEY,
                        equipment_id    INT NOT NULL,
                        used_by         INT,                  
                        used_at         DATETIME DEFAULT NOW(),
                        duration_mins   INT,
                        FOREIGN KEY (equipment_id) REFERENCES equipment(id)
                    );
                ''')
                # used_by -- member_id, nullable
                

                conn.commit()
                # Updated logging message to be more accurate
                logging.info("All tables for GymMonk have been checked/created successfully.")

    except Error as e:
        logging.error(f"Error during database setup: {e}")
        raise

if __name__ == '__main__':
    logging.info("Starting database setup...")
    setup_database()
