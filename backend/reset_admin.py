import os
import mysql.connector
from dotenv import load_dotenv
from core.security import hash_password

load_dotenv()

def reset_password(username, new_password):
    """
    Updatesthe password for an existing admin user in the GymDB database.
    """
    print(f"--- Reseting Password for Admin: {username} ---")

    hashed_pw = hash_password(new_password)

    try:
        conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = os.getenv('MYSQL_PASSWORD'),
            database = 'GymDB'
        )
        cursor = conn.cursor()

        query = "UPDATE ADMIN SET password = %s WHERE username = %s"
        cursor.execute(query, (hashed_pw,username))
        conn.commit()

        if cursor.rowcount > 0:
            print(f"✅ SUCCESS: Password for '{username}' has been updated.")
            print(f"You can now login with your new password.")
        else:
            print(print(f"❌ FAILED: Admin username '{username}' not found in the database."))
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    # --- CONFIGURATION ---
    """
    target_username = "bokaria2062@gmail.com"  # Change this if your username is different
    new_admin_password = "Hellogopu@19" # Set your desired new password here
    # ---------------------
    
    reset_password(target_username, new_admin_password)
    """