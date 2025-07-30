import bcrypt

def hash_password(password: str) -> str:
    """Hashes a password using bcrypt and returns it as a string."""
    salt = bcrypt.gensalt()
    hashed_password_bytes = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password_bytes.decode('utf-8') # Decode bytes to string

def verify_password(plain_password: str, hashed_password_str: str) -> bool:
    """Verifies a plain password against a hashed string password."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password_str.encode('utf-8'))
