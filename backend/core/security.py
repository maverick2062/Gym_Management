import bcrypt
import logging

# Configure logging for the security module
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def hash_password(password: str) -> str:
    """
    Generates a bcrypt hash of a plain-text password.

    This function takes a plain-text password, generates a salt,
    and then hashes the password with the salt. The resulting hash
    is decoded to a UTF-8 string so it can be easily stored in the database.

    Args:
        password (str): The user's plain-text password.

    Returns:
        str: The hashed password as a string, ready for database storage.
    """
    try:
        # Encode the password string to bytes, which is required by bcrypt
        password_bytes = password.encode('utf-8')
        # Generate a salt to protect against rainbow table attacks
        salt = bcrypt.gensalt()
        # Hash the password with the generated salt
        hashed_pw_bytes = bcrypt.hashpw(password_bytes, salt)
        # Decode the resulting bytes back to a string for storage
        return hashed_pw_bytes.decode('utf-8')
    except Exception as e:
        logging.error(f"Error occurred during password hashing: {e}")
        raise

def verify_password(plain_password: str, hashed_password_str: str) -> bool:
    """
    Verifies a plain-text password against a stored bcrypt hash.

    This function compares a plain-text password with a hash retrieved
    from the database. It encodes both to bytes before checking.

    Args:
        plain_password (str): The raw password entered by the user for verification.
        hashed_password_str (str): The hashed password retrieved from the database.

    Returns:
        bool: True if the password matches the hash, False otherwise.
    """
    try:
        # Encode both the plain password and the stored hash to bytes
        plain_password_bytes = plain_password.encode('utf-8')
        hashed_password_bytes = hashed_password_str.encode('utf-8')
        # Use bcrypt's checkpw function to securely compare them
        return bcrypt.checkpw(plain_password_bytes, hashed_password_bytes)
    except Exception as e:
        logging.error(f"Error occurred during password verification: {e}")
        # Return False in case of an error to prevent potential security bypasses
        return False


