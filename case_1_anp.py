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
