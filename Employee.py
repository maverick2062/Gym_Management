import mysql.connector as sql
from mysql.connector import Error
import bcrypt
import time
import random
from datetime import date
import getpass
import Product_M as PM
import db_check as status

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
    if status.check()==0:
        con = sql.connect(
        host='localhost',
        user='root',
        password='tiger@99',
        database='Inventory'
        )
        
        if con.is_connected():
            time.sleep(0.5)
            print("\nConnected to Inventory Database!")
        cur=con.cursor()      
        
        cur.execute('''
            CREATE TABLE IF NOT EXISTS EMPL(
                emp_ID int AUTO_INCREMENT PRIMARY KEY,
                Name varchar(50) NOT NULL,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(25) NOT NULL
            );
        ''')
        
        cur.execute('''
            CREATE TABLE IF NOT EXISTS ELD(
                login_id int AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL,
                emp_id int,
                login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                emp_status ENUM('active','deactive') DEFAULT 'active',
                login_status varchar(30) NOT NULL DEFAULT 'Login Successfull',
                FOREIGN KEY (emp_id) REFERENCES ADMIN(emp_ID) ON DELETE CASCADE
            );
        ''')
        con.commit()

        time.sleep(0.5)
        print("\n\n\t\tTABLES CHECKED/CREATED SUCCESSFULLY.")
        return con
        
    else:
        return sql.connect(
            host='localhost',
            user='root',
            password='tiger@99',
            database='Inventory'
            )

def username_exists(username):
    con = connect_db()
    cur = con.cursor()
    cur.execute("SELECT username FROM EMPL WHERE username = '{}'".format(username))
    res = cur.fetchone()
    cur.close()
    con.close()
    return res is not None

def sign_up():
    con = connect_db()
    cur=con.cursor()

    restart = 'y'
    while restart == 'y' or restart == 'Y':
        time.sleep(0.15)
        print("\n\t\t -----EMPLOYEE REGISTRATION----- ")
        
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
                if password!=con_pass:
                    print("\n\t\tPasswords do not match! Please try again.")
                    return inco_pass
                else:
                    return password

        password = inco_pass()
        hashed_pass = bcrypt.hashpw(password.encode(),bcrypt.gensalt())
        name = input("Enter your Name: ")

        cur.execute(
    "INSERT INTO EMPL (Name, username, password) VALUES ('{}', '{}', '{}')".format(name, username, password)
        )
        con.commit()
        print("EMPLOYEE Added!!")
        
        cur.close()
        con.close()
        
        time.sleep(0.5)
        print("\nRedirecting to the Login Page")
        time.sleep(0.5)
        login()

def authenticate_user(username, password):
    con = connect_db()
    cur = con.cursor()
    
    try:
        # Use parameterized query to prevent SQL injection
        # Retrieve both password and ad_ID
        cur.execute(
            "SELECT emp_ID, password FROM EMPL WHERE username = %s", (username,)
        )
        res = cur.fetchone()
        
        if res is None:
            em = "Invalid Username"
            cur.execute(
                "INSERT INTO ELD (username, login_status) VALUES (%s, %s)", 
                (username, em)
            )
            con.commit()
            return em 
        else:
            emp_id = res[0] 
            stored_password = res[1]
            
            if password != stored_password:
                em = "Invalid Password"
                cur.execute(
                    "INSERT INTO ELD (username, emp_id, login_status) VALUES (%s, %s, %s)", 
                    (username, emp_id, em)
                )
                con.commit()
                return em
            else:
                em = "Login Successfully"
                cur.execute(
                    "INSERT INTO ELD (username, emp_id, login_status) VALUES (%s, %s, %s)", 
                    (username, emp_id,em)
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
            print("\n\n\tEMPLOYEE VERIFIED✅")
            cur.execute("select Name,emp_id from empl where username='{}'".format(username,))
            res=cur.fetchall()
            emp_ID=res[1]
            print("      __________________________________________________")
            print()
            print('\t \t \t SUCCESSFULLY LOGIN!!\n\t ____________________________________________')
            print()
            print(' \n\t\tWelcome',res[0], 'to the Inventory')
            print("\t\t   ************************************")
            print()
            LD=input("\n\t Login Details(Y/N)")
            if LD.upper()== 'Y':
                login_details(username,emp_ID)
            PM.menu()
            break
                    
        else:
            print("INVALID CREDENTIALS ❌")
            restart=input("\n\t\tDo you wish to login again?(y/n): ")
            
    cur.close()
    con.close()
    
def login_details(username,emp_ID):
    
    con = connect_db()
    cur = con.cursor()
    
    cur.execute("SELECT * FROM ELD WHERE username = %s and emp_id = %s", 
            (str(username), str(emp_ID)))
    res=cur.fetchall()

    if res:
        print("\n\n{:^85}".format(" EMPLOYEE LOGIN DETAILS"))
        print("{:^90}".format("||======================================||\n"))

        print("|---------------------------------------------------------------------------------------------|")
        print(f"| {'ID':<5} | {'username':<20} | {'emp_id':<5} | {'login_time':<20} | {'emp_status':<10} | {'login_status':<20}")
        print("|---------------------------------------------------------------------------------------------|")

        for rest in res:
            login_time = rest[3]
            formatted_time = login_time.strftime('%Y-%m-%d %H:%M:%S') if login_time else ""
            print(f"| {rest[0]:<5} | {rest[1]:<20} | {rest[2]:<5} | {formatted_time:<20} | {rest[4]:<10} | {rest[5]:<20}")
            print("|---------------------------------------------------------------------------------------------|\n")
        print("{:^90}".format("||======================================||"))

            
