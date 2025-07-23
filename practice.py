import mysql.connector as sql
from mysql.connector import Error 

try:
    # Establish initial connection without specifying a database
    con = sql.connect(
        host='localhost',
        user='root',
        password='tiger@99'
    )

    if con.is_connected():
        print("\n\tConnection Successfully established with MYSQL SERVER!")
        db_info = con.get_server_info()
        print(f"\n\t\tConnected to MySQL Server version {db_info}")

    cur = con.cursor()
            
    # Create the database if it doesn't exist
    cur.execute("CREATE DATABASE IF NOT EXISTS Inventory")
    print("\n\n\t\tDATABASE INVENTORY CHECKED/CREATED")
          
    cur.close()
    con.close()
          
    # Reconnect to the created database

    con = sql.connect(
    host='localhost',
    user='root',
    password='tiger@99',
    database='Inventory'
    )

    if con.is_connected():
          print("\nConnected to Inventory Database!")
    cur=con.cursor()      

    cur.execute('''
        CREATE TABLE IF NOT EXISTS PRODUCT(
            p_code int(3) Primary Key,
            p_name varchar(30),
            p_qty int(5),
            p_up int(7),
            p_cat varchar(30)
        );
    ''')
    con.commit()

    print("\n\n\t\tTABLE PRODUCT CHECKED/CREATED SUCCESSFULLY.")

except Error as e:
    print(f"Error while connecting to MySQL: {e}")


class DuplicateError(Exception):
    """Custom exception for duplicate product code."""
    pass

def anp():
    
    try:
        cur=con.cursor()
        p_code=int(input("\nEnter Product Code: "))
            
        cur.execute("SELECT p_code FROM PRODUCT WHERE p_code = %s", (p_code,))
        existing_product = cur.fetchone()  # Returns a tuple like (101,) or None

        if existing_product:
            raise DuplicateError("\n\t\t⚠️ Duplicate Product Code")
        
        p_name=input("\nEnter Product Name: ")
        p_qty=int(input("\nEnter Product Quantity: "))
        p_up=int(input("\nEnter Product Unit Price: "))
        p_cat=input("\nEnter Product Category: ")

        cur.execute("INSERT INTO PRODUCT VALUES (%s, %s, %s, %s, %s);", (p_code, p_name, p_qty, p_up, p_cat))
        con.commit()
        print("\n\t\tNEW RECORD ADDED TO THE TABLE")
        
    except DuplicateError as e:
        print(e)
        
    except Error as e:
        print(f"{e}")

def lap():
    cur = con.cursor()
    print("\n|-----------------------------------------------------------------------------------|")
    
    cur.execute("SELECT * FROM PRODUCT")
    rows = cur.fetchall()  # Fetch all rows from the query

    if not rows:
        print("\nNo products found in the inventory.")
    else:
        print("|\t\t\t\tPRODUCT LIST\t\t\t\t\t    |")
        print("|-----------------------------------------------------------------------------------|")
        #print(f"{'Code':<10}{'Name':<30}{'Qty':<10}{'Price':<10}{'Category':<20}")
        #print("{:<10}{:<30}{:<10}{:<10}{:<20}".format("Code", "Name", "Qty", "Price", "Category"))
        print("| %-10s%-30s%-10s%-10s%-20s  |" % ("Code", "Name", "Qty", "Price", "Category"))
        print("|-----------------------------------------------------------------------------------|")
        for row in rows:
            #print(f"{row[0]:<10}{row[1]:<30}{row[2]:<10}{row[3]:<10}{row[4]:<20}")
            #print("{:<10}{:<30}{:<10}{:<10}{:<20}".format(row[0], row[1], row[2], row[3], row[4]))
            print("| %-10s%-30s%-10s%-10s%-20s  |" % (row[0], row[1], row[2], row[3], row[4]))

    print("|","\t"*10,"   |")
    print("|-----------------------------------------------------------------------------------|")


def L_prod_qty(choi):
    try:
        cur = con.cursor()
        if choi == 1:
            cur.execute("SELECT * FROM PRODUCT ORDER BY p_qty ASC")
            result = cur.fetchall()
            
        elif choi == 2:
            cur.execute("SELECT * FROM PRODUCT ORDER BY p_qty DESC")
            result = cur.fetchall()
            
        elif choi == 3:
            a=int(input("\nEnter lower limit: "))
            b=int(input("\nEnter upper limit: "))
            
            a=min(a,b)
            b=max(a,b)

            cur.execute("SELECT * FROM PRODUCT WHERE p_qty BETWEEN %s and %s",(a,b))
            result = cur.fetchall()
            
        elif choi == 4:
            sp_qty=int(input("\nEnter your specific quantity: "))
            cur.execute("SELECT * FROM PRODUCT WHERE p_qty = %s",(sp_qty,))
            result = cur.fetchall()

        # Display Result
        if result:
            print("\n|---------------------------------------------------------------------------------------|")
            print(f"| {'Qty':<10} | {'Name':<30} | {'Code':<10} | {'Price':<10} | {'Category':<20}")
            print("|---------------------------------------------------------------------------------------|")

            for res in result:
                print(f"| {res[2]:<10} | {res[1]:<30} | {res[0]:<10} | {res[3]:<10} | {res[4]:<20}")
            print("|---------------------------------------------------------------------------------------|")
        else:
            print("\n❌ No products found .")

    except ValueError:
        print("Invalid entry. Please enter a number.")


def Catwise_Prod():
    
    try:
        cur = con.cursor()
        CAT=input("\n\t\tEnter product category: ")
        cur.execute("SELECT * FROM PRODUCT WHERE p_cat = %s", (CAT,))
        result = cur.fetchall()

        # Display Result
        if result:
            print("\n\t\t\t\t✅ Product Found")
            print("\n|---------------------------------------------------------------------------------------|")
            print(f"| {'Category':<20} | {'Name':<30} | {'Qty':<10} | {'Price':<10} | {'Code':<10}")
            print("|---------------------------------------------------------------------------------------|")

            for res in result:
                print(f"| {res[4]:<20} | {res[1]:<30} | {res[2]:<10} | {res[3]:<10} | {res[0]:<10}")
            print("|---------------------------------------------------------------------------------------|")
        else:
            #Printing Messages
            print("\n\t\t\t❌ No product found under this category.")

            #Displaying Available Categories for Users Reference
            print("\n\n{:^80}".format("📦 Available Product Categories"))
            print("{:^80}".format("||======================================||"))

            #Executing the query
            cur.execute("SELECT p_cat FROM PRODUCT")
            
            res = cur.fetchall()
            
            for cat in res:
                print(f"{cat[0]:^80}")
            print("{:^80}".format("||======================================||"))

    #Error Handling
            
    except ValueError:
        print("Invalid entry. Please enter a string.")

def up_prod():
    try:
        cur=con.cursor()
        
        code=int(input("\n\tEnter Product Code which requires modification: "))
        valid_col = ['p_code','p_name','p_qty','p_up','p_cat']
        col = input("\n\t🔹 Enter the column name to update (p_code,p_name, p_qty, p_up,p_cat): ").strip()

        if col not in valid_col:
            print("\n❌ Invalid column name. Please enter a valid column (p_code,p_name, p_qty, p_up,p_cat).")
            return
        
        up=input("\nEnter your modification for the product: ").strip()

        if col in ['p_code','p_qty','p_up']:
            try:
                up = int(up)
            except ValueError:
                print("\n❌ Invalid input! Please enter a valid number.")
                return
            
        query = f"UPDATE PRODUCT SET {col} = %s WHERE p_code = %s"
        cur.execute(query, (up, code))
        con.commit()

        
        cur.execute("SELECT * FROM PRODUCT WHERE p_code = %s",(code,))
        res=cur.fetchall()

        if res:
            print("\n\n{:^80}".format("🛠 UPDATED PRODUCT DETAILS"))
            print("{:^80}".format("||======================================||\n"))

            print("|---------------------------------------------------------------------------------------|")
            print(f"| {'Code':<10} | {'Name':<30} | {'Qty':<10} | {'Price':<10} | {'Category':<20}")
            print("|---------------------------------------------------------------------------------------|")

            for rest in res:
                print(f"| {rest[0]:<10} | {rest[1]:<30} | {rest[2]:<10} | {rest[3]:<10} | {rest[4]:<20}")

            print("|---------------------------------------------------------------------------------------|\n")
            print("{:^80}".format("||======================================||"))

        else:
            print("\n❌ No product found with the given code.")
            
    except ValueError:
        print("\n❌ Invalid input. Please enter valid data types.")
    except Exception as e:
        print(f"\n❌ Error updating product: {e}")
    finally:
        cur.close()


def del_prod():
    try:
        cur=con.cursor()
        code=int(input("\n\tEnter Product Code needed to be deleted: "))

        cur.execute("SELECT p_code FROM PRODUCT WHERE p_code = %s",(code,))
        res = cur.fetchone()
       
        if res:
            cur.execute("DELETE FROM PRODUCT WHERE p_code = %s",(code,))
            con.commit()
            print("\n\tPRODUCT DELETED SUCCESSFULLY")
        else:
            print("\n\t\t❌ No product found with the given code.")
            return

    except ValueError:
        print("\n❌ Invalid input. Please enter valid data types.")
    except Exception as e:
        print(f"\n❌ Error Deleting product: {e}")
    finally:
        cur.close()


ch='y' or 'Y'
while ch.lower() == 'y':
    
    print("\n\t\t\tSALES INVENTORY MANAGEMENT")
    print("\t\t   ***********************************")
    print("\n\t\t1.) PRODUCT MANAGEMENT")
    print("\n\t\t2.) PURCHASE MANAGEMENT")
    print("\n\t\t3.) SALES MANAGEMENT")
    print("\n\t\t4.) EXIT")

    try:
        c = int(input("\nEnter your choice: "))
    except ValueError:
        print("Invalid entry. Please enter a number.")
        continue

    match c:
        case 1:
            print("\n\t\t1) ADD NEW PRODUCT")
            print("\n\t\t2) LIST PRODUCT")
            print("\n\t\t3) UPDATE PRODUCT")
            print("\n\t\t4) DELETE PRODUCT")
            print("\n\t\t5) EXIT")
            try:
                cho = int(input("\nEnter your choice: "))
                match cho:
                    case 1:
                        anp()
                    case 2:
                        print("\n\t\t --------------------------------- ")
                        print("\n\t\t| 1 | LIST ALL PRODUCTS           |")
                        print("\n\t\t| 2 | LIST PRODUCTS QUANTITY WISE |")
                        print("\n\t\t| 3 | LIST PRODUCTS CATEGORY WISE |")
                        print("\n\t\t --------------------------------- ")
                        try:
                            cho = int(input("\nEnter your choice: "))
                            match cho:
                                case 1:
                                    lap()
                                case 2:
                                    print("\n\t\t\t --------------------------------- ")
                                    print("\n\t\t\t| 1 | IN ASCENDING ORDER          |")
                                    print("\n\t\t\t| 2 | IN DESCENDING ORDER         |")
                                    print("\n\t\t\t| 3 | IN A DEFINITE RANGE         |")
                                    print("\n\t\t\t| 4 | PRODUCTS WITH SPECIFIC QTY  |")
                                    print("\n\t\t\t --------------------------------- ")
                                    choi=int(input("\n\t\tEnter your choice: "))
                                    L_prod_qty(choi)
                                case 3:
                                    Catwise_Prod()
                                case _:
                                    print("Invalid choice in Purchase Management.")
                                    
                        except ValueError:
                            print("Invalid entry. Please enter a number.")
                            
                    case 3:
                        up_prod()
                    case 4:
                        del_prod()
                    case 5:
                        break
                    case _:
                        print("Invalid choice in Product Management.")
            except ValueError:
                print("Invalid entry. Please enter a number.")
##        case 2:
            
        case 5:
            print("Exiting...")
            con.close()
            break
        case _:
            print("Invalid Entry in Main Menu.")
    
    ch = input("\nDo you wish to visit the main menu (Y/N)? ")
    if ch.lower() == 'n':
        con.close()
        print("\n\t\tExiting... Database connection closed.")
        break

        



        

