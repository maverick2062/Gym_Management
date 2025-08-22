import db_check as db
import admin 
import Employee
import time

ch='y'
while ch.lower() == 'y':
    time.sleep(0.3)
    sql_pass=input("\n\t\tSQL PASSWORD: ")
    time.sleep(0.3)
    db.connect(sql_pass)
    time.sleep(0.3)
    print("\n\t\t     WELCOME TO SALES INVENTORY MANAGEMENT SYSTEM!")
    time.sleep(0.3)
    print("\t\t\t *************************************")
    time.sleep(0.3)
    print("\n\t\t\t\t1.) ADMIN ")
    print("\n\t\t\t\t2.) EMPLOYEE ")
    print("\n\t\t\t\t3.) EXIT")

    try:
        c = int(input("\nEnter your choice: "))
    except ValueError:
        print("Invalid entry. Please enter a number.")
        continue
    
    match c:
        case 1:
            print("\n\t\t ------------- ")
            print("\n\t\t| 1 | LOG IN  |")
            print("\n\t\t| 2 | SIGN UP |")
            print("\n\t\t ------------- ")
            
            cho = int(input("\nEnter your choice: "))
            if cho == 1:
                admin.login(sql_pass)
            elif cho == 2:
                admin.sign_up()
        case 2:
            print("\n\t\t ------------- ")
            print("\n\t\t| 1 | LOG IN  |")
            print("\n\t\t| 2 | SIGN UP |")
            print("\n\t\t ------------- ")
            if cho == 1:
                Employee.login(sql_pass)
            elif cho == 2:
                Employee.sign_up(sql_pass)
        case 3:
            print("Exiting...")
            break
        case _:
            print("Invalid Entry in Main Menu.")
    
    ch = input("\nDo you wish to visit the main menu (Y/N)? ")
    if ch.lower() == 'n':
        print("\n\t\tExiting... Database connection closed.")
        break
            
