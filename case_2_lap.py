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
