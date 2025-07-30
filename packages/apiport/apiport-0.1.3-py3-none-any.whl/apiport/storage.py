"""
Storage module for the apiport CLI tool.
"""
import os
import json
import sys

from .encryption import encrypt, decrypt

VAULT_PATH = os.path.expanduser("~/.apiport/vault.port")

def load_vault():
    """Load the vault from disk.
    
    Returns:
        dict: The loaded vault, or an empty dict if the vault doesn't exist.
    """
    if not os.path.exists(VAULT_PATH):
        return {}
    with open(VAULT_PATH, "rb") as f:
        decrypted = decrypt(f.read())
        return json.loads(decrypted)

def save_vault(data: dict):
    """Save the vault to disk.
    
    Args:
        data: The vault data to save.
    """
    os.makedirs(os.path.dirname(VAULT_PATH), exist_ok=True)
    with open(VAULT_PATH, "wb") as f:
        f.write(encrypt(json.dumps(data).encode()))
