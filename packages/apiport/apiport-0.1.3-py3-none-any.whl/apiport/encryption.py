"""
Encryption module for the apiport CLI tool.
"""
from cryptography.fernet import Fernet
import os

KEY_PATH = os.path.expanduser("~/.apiport_key")

def get_key():
    """Get the encryption key.
    
    Returns:
        bytes: The encryption key.
    """
    if os.path.exists(KEY_PATH):
        with open(KEY_PATH, "rb") as f:
            return f.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_PATH, "wb") as f:
            f.write(key)
        return key

def encrypt(data: bytes) -> bytes:
    """Encrypt data using Fernet symmetric encryption.
    
    Args:
        data: The data to encrypt.
        
    Returns:
        bytes: The encrypted data.
    """
    return Fernet(get_key()).encrypt(data)

def decrypt(data: bytes) -> bytes:
    """Decrypt data using Fernet symmetric encryption.
    
    Args:
        data: The data to decrypt.
        
    Returns:
        bytes: The decrypted data.
    """
    return Fernet(get_key()).decrypt(data)
