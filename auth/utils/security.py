import hashlib

def password_encode(password: str) -> str:
    """Encode password using SHA-1"""
    # Create SHA-1 hash object
    sha1_hash = hashlib.sha1()
    
    # Update hash object with password bytes
    sha1_hash.update(password.encode('utf-8'))
    
    # Get hexadecimal digest
    hashed = sha1_hash.hexdigest()
    
    return hashed

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against SHA-1 hashed password"""
    # Hash the plain password
    sha1_hash = hashlib.sha1()
    sha1_hash.update(plain_password.encode('utf-8'))
    calculated_hash = sha1_hash.hexdigest()
    
    # Compare the calculated hash with the stored hash
    return calculated_hash == hashed_password