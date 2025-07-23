import os

def check():
    filename = "check.txt"
    
    # First check if the file exists and its size
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        return 1
    else:
        # Open the file only if we need to write to it
        with open(filename, "a") as f:
            f.write("YES")
        return 0

def connect(sql_pass):
    try:
        # Establish initial connection without specifying a database
        con = sql.connect(
            host='localhost',
            user='root',
            password=sql_pass
        )

        if con.is_connected():
            time.sleep(0.5)
            print("\n\tConnection Successfully established with MYSQL SERVER!")
            db_info = con.get_server_info()
            time.sleep(0.5)
            print(f"\n\t\tConnected to MySQL Server version {db_info}")
        else:
            exit()

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
