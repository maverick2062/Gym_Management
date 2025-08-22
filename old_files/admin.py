import mysql.connector as sql
from mysql.connector import Error
import bcrypt
import time
import random
from datetime import date
import getpass
import Product_M as PM
import db_check as status

def connect_db(sql_pass):
    if status.check()==0:
        con = sql.connect(
        host='localhost',
        user='root',
        password=sql_pass,
        database='Inventory'
        )
        
##        if con.is_connected():
##            time.sleep(0.5)
##            print("\nConnected to Inventory Database!")
        cur=con.cursor()      
        
        cur.execute('''
            CREATE TABLE IF NOT EXISTS ADMIN(
                ad_ID int AUTO_INCREMENT PRIMARY KEY,
                Name varchar(50) NOT NULL,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(100) NOT NULL
            );
        ''')
        
        cur.execute('''
            CREATE TABLE IF NOT EXISTS ALD(
                login_id int AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL,
                ad_id int,
                login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                user_status ENUM('active','deactive') DEFAULT 'active',
                login_status varchar(30) NOT NULL DEFAULT 'Login Successfull',
                FOREIGN KEY (ad_id) REFERENCES ADMIN(ad_ID) ON DELETE CASCADE
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
            password=sql_pass,
            database='Inventory'
            )

def username_exists(username,sql_pass):
    con = connect_db(sql_pass)
    cur = con.cursor()
    cur.execute("SELECT username FROM ADMIN WHERE username = %s",(username,))
    res = cur.fetchone()
    cur.close()
    con.close()
    return res is not None

def sign_up(sql_pass):
    con = connect_db(sql_pass)
    cur=con.cursor()

    restart = 'y'
    while restart == 'y' or restart == 'Y':
        time.sleep(0.15)
        print("\n\t\t -----ADMIN REGISTRATION----- ")
        
        def user_name():
            username = input("Enter username: ")
            if username_exists(username,sql_pass):
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
                    return inco_pass()
                else:
                    return password

        password = inco_pass()
        hashed_pass = bcrypt.hashpw(password.encode(),bcrypt.gensalt())
        name = input("Enter your Name: ")

        cur.execute(
    "INSERT INTO ADMIN (Name, username, password) VALUES (%s,%s,%s)",(name, username, hashed_pass)
        )
        con.commit()
        print("Admin Added!!")
        
        cur.close()
        con.close()
        
        time.sleep(0.5)
        print("\nRedirecting to the Login Page")
        login(sql_pass)

def authenticate_user(username, password,sql_pass):
    con = connect_db(sql_pass)
    cur = con.cursor()
    
    try:
        cur.execute(
            "SELECT ad_ID, password FROM ADMIN WHERE username = %s", (username,)
        )
        res = cur.fetchone()
        
        if res is None:
            em = "Invalid Username"
            cur.execute(
                "INSERT INTO ALD (username, login_status) VALUES (%s, %s)", 
                (username, em)
            )
            con.commit()
            return em 
        else:
            admin_id = res[0]
            stored_password = res[1].encode('utf-8')
            
            if not bcrypt.checkpw(password.encode('utf-8'), stored_password): 
                em = "Invalid Password"
                cur.execute(
                    "INSERT INTO ALD (username, ad_id, login_status) VALUES (%s, %s, %s)", 
                    (username, admin_id, em)
                )
                con.commit()
                return em
            else:
                em = "Login Successfully"
                cur.execute(
                    "INSERT INTO ALD (username, ad_id, login_status) VALUES (%s, %s, %s)", 
                    (username, admin_id,em)
                )
                con.commit()
                return True
    finally:
        # Ensure resources are cleaned up even if an error occurs
        cur.close()
        con.close()
    
            
def login(sql_pass):
    con = connect_db(sql_pass)
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
        verify = authenticate_user(username,password,sql_pass)
        
        if verify == True:
            print("\n\n\tADMIN VERIFIED✅")
            cur.execute("select Name from admin where username=%s",(username,))
            customer=cur.fetchone()
            cur.execute("select ad_id from admin where username=%s",(username,))
            res=cur.fetchone()
            ad_ID=res[0]
            print("      __________________________________________________")
            print()
            print('\t \t \t SUCCESSFULLY LOGIN!!\n\t ____________________________________________')
            print()
            print(' \n\t\tWelcome',customer[0], 'to the Inventory')
            print("\t\t   ************************************")
            print()
            LD=input("\n\t Login Details(Y/N)")
            if LD.upper()== 'Y':
                login_details(username,ad_ID,sql_pass)
            PM.menu()
            break
                    
        else:
            print("INVALID CREDENTIALS ❌")
            restart=input("\n\t\tDo you wish to login again?(y/n): ")
            
    cur.close()
    con.close()
    
def login_details(username,ad_ID,sql_pass):
    
    con = connect_db(sql_pass)
    cur = con.cursor()
    
    cur.execute("SELECT * FROM ALD WHERE username = %s and ad_id = %s", 
            (str(username), str(ad_ID)))
    res=cur.fetchall()

    if res:
        print("\n\n{:^85}".format(" ADMIN LOGIN DETAILS"))
        print("{:^90}".format("||======================================||\n"))

        print("|---------------------------------------------------------------------------------------------|")
        print(f"| {'ID':<5} | {'username':<20} | {'ad_id':<5} | {'login_time':<20} | {'user_status':<10} | {'login_status':<20}")
        print("|---------------------------------------------------------------------------------------------|")

        for rest in res:
            login_time = rest[3]
            formatted_time = login_time.strftime('%Y-%m-%d %H:%M:%S') if login_time else ""
            print(f"| {rest[0]:<5} | {rest[1]:<20} | {rest[2]:<5} | {formatted_time:<20} | {rest[4]:<10} | {rest[5]:<20}")
            print("|---------------------------------------------------------------------------------------------|\n")
        print("{:^90}".format("||======================================||"))

            
