import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import your Admin class and the database setup function
from api.admin import Admin
from database.connection import setup_database

def create_first_admin():
    """
    A one-time script to create the initial administrator account
    with a properly hashed password.
    """
    print("--- Setting up database and creating initial admin ---")
    
    # First, ensure the database and tables exist
    setup_database()

    # --- CONFIGURE YOUR ADMIN DETAILS HERE ---
    admin_name = "NIKHIL BOKARIA"
    admin_username = "bokaria2062@gmail.com"
    admin_password = "Hellogopu@19" # Choose a secure password
    # -----------------------------------------

    print(f"Attempting to create admin with username: '{admin_username}'")

    # Check if the admin already exists to avoid errors on re-running
    if Admin.username_exists(admin_username):
        print(f"Admin username '{admin_username}' already exists. Skipping creation.")
        return

    # Use the Admin.create method which handles password hashing
    new_admin = Admin.create(
        name=admin_name,
        username=admin_username,
        password=admin_password
    )

    if new_admin:
        print("\n✅ SUCCESS: Admin account created successfully!")
        print(f"   - Username: {new_admin.username}")
        print("   - You can now log in with the password you set in this script.")
    else:
        print("\n❌ FAILED: Could not create admin account.")
    
    print("----------------------------------------------------")


if __name__ == '__main__':
    create_first_admin()
