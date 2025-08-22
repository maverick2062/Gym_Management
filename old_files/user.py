import mysql.connector as sql
from mysql.connector import Error
import bcrypt
import time
import random
from datetime import date

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def register(self):
        sign_up()

def connect():
    try:
        # Establish initial connection without specifying a database
        con = sql.connect(
            host='localhost',
            user='root',
            password='tiger@99'
        )

        if con.is_connected():
            time.sleep(0.5)
            print("\n\tConnection Successfully established with MYSQL SERVER!")
            db_info = con.get_server_info()
            time.sleep(0.5)
            print(f"\n\t\tConnected to MySQL Server version {db_info}")

        cur = con.cursor()
                
        # Create the database if it doesn't exist
        cur.execute("CREATE DATABASE IF NOT EXISTS Inventory")
        time.sleep(0.5)
        print("\n\n\t\tDATABASE INVENTORY CHECKED/CREATED")
              
        cur.close()
        con.close()

    except Error as e:
        time.sleep(0.2)
        print(f"Error while connecting to MySQL: {e}")

def connect_db():
    global i
    
    if not globals().get('i', 0):

        i=1
        
        con = sql.connect(
        host='localhost',
        user='root',
        password='tiger@99',
        database='Inventory'
        )
        
        if con.is_connected():
            time.sleep(0.5)
            print("\nConnected to Inventory Database!")
        cur = con.cursor()

        cur.execute('''
            CREATE TABLE IF NOT EXISTS USER(
                us_ID int AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(25) NOT NULL
            );
        ''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS ULD(
                login_id int AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                us_id int,
                login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                user_status ENUM('active','deactive') DEFAULT 'active',
                FOREIGN KEY (us_id) REFERENCES USER(us_ID)
            );
        ''')
        con.commit()

        time.sleep(0.5)
        print("\n\n\t\tTABLES CHECKED/CREATED SUCCESSFULLY.")
        
    else:
        return sql.connect(
            host='localhost',
            user='root',
            password='tiger@99',
            database='Inventory'
            )

def username_exists(username):
    con = connect_db()
    if not con:
        #Handles connection failures 
        return False
    cur = con.cursor()
    cur.execute("SELECT username FROM USER WHERE username = %s",(username,))
    res = cur.fetchone()
    cur.close()
    con.close()
    return res is not None

def sign_up():
    con = connect_db()
    cur = con.cursor()

    restart = 'y'
    while restart == 'y' or restart == 'Y':
        time.sleep(0.15)
        print("\n\t\t -----USER REGISTRATION----- ")
        
        def user_name():
            username = input("Enter username: ")
            if username_exists(username):
                time.sleep(0.2)
                print("\nUsername already exists! Please try a different one.")
                return user_name()
            else:
                return username
        username = user_name()
        
        # Password Input with validation
        def inco_pass():
            
            password = input('\nEnter LOGIN Password you desire (only 8 characters) : ')
            
            if len(password) != 8:
                print("\n\t\tPassword must be of 8 characters...\nKindly Enter again")
                return inco_pass()
            
            else:
                con_pass=input('\nConfirm your password : ')
                if password!=conpass:
                    print("\n\t\tPasswords do not match! Please try again.")
                    return inco_pass
                else:
                    return password

        password = inco_pass()
        hashed_pass = bcrypt.hashpw(password.encode(),bcrypt.gensalt())
        name = input("Enter your Name: ")

        cur.execute(
    "INSERT INTO USER (Name, username, password) VALUES (%s, %s, %s)",(name, username, password)
        )
        
        con.commit()
        print("USER Added!!")
        print()


def authenticate_user(username,password):
    con = connect_db()
    cur = con.cursor()
    
    try:
        
        cur.execute(
            "SELECT us_id, password FROM USER WHERE username = %s", (username,)
        )
        us_ID = cur.fetchone()
        
        if res is None:
            em = "Invalid Username"
            cur.execute(
                "INSERT INTO ULD (username, us_id, login_status) VALUES (%s, %s, %s)", 
                (username, us_ID, em)
            )
            con.commit()
            return em 
        else:
            user_id = res[0]  # Get the admin_id
            stored_password = res[1]
            
            if password != stored_password:
                em = "Invalid Password"
                cur.execute(
                    "INSERT INTO ULD (username, us_id, login_status) VALUES (%s, %s, %s)", 
                    (username, user_id, em)
                )
                con.commit()
                return em
            else:
                em = "Login Successfull"
                cur.execute(
                    "INSERT INTO ULD (username, ud_id, login_status) VALUES (%s, %s, %s)", 
                    (username, user_id, em)
                )
                con.commit()
                return True
    finally:
        # Ensure resources are cleaned up even if an error occurs
        cur.close()
        con.close()
        
def login():
    con = connect_db()
    cur = con.cursor()
    
    restart='y'
    while restart=='y' or restart=='Y':
        print()
        time.sleep(0.3)
        print("\t\t-----------Login-------------")
        print()
        
        username=input('Enter your username: ')
        password=input('Enter your password: ')

        time.sleep(0.3)    
        print("\n\t\tAUTHENTICATING CREDENTIALS")
        verify = authenticate_user(username,password)
        
        if verify == True:
            print("USER VERIFIED✅")
            cur.execute("select Name from admin where username='{}'".format(username,))
            customer=cur.fetchone()
            print("      __________________________________________________")
            print()
            print('\t \t \t SUCCESSFULLY LOGIN!!\n\t ____________________________________________')
            print()
            print(' Welcome',customer, 'to the Inventory')
            print("   ************************************")
            print()
            PM.menu()
                    
        else:
            print("INVALID CREDENTIALS ❌")
            restart=input("\n\t\tDo you wish to login again?(y/n): ")
            
    cur.close()
    con.close()
