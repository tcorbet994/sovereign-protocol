import os
import base64
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def generate_key_encryption_key():
    """Generate a key to encrypt the owner key"""
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(b"SOVEREIGN_CONTROL"))
    return key, salt

def encrypt_owner_key(key_data):
    """Encrypt the owner key"""
    key, salt = generate_key_encryption_key()
    f = Fernet(key)
    encrypted_data = f.encrypt(key_data.encode())
    return encrypted_data, salt

def store_encrypted_key():
    """Store the encrypted owner key"""
    # The key is processed through multiple layers of encryption before storage
    key_data = "WRBWV_nP`5]Y?j]PTRah}m*$iW{%B$%rFtCNkqEd4ZadS2UDBEkBGJKDF8pwtLOw"
    
    # First layer: Hash the key
    key_hash = hashlib.sha3_512(key_data.encode()).digest()
    
    # Second layer: Encrypt the hash
    encrypted_key, salt = encrypt_owner_key(base64.b64encode(key_hash).decode())
    
    # Store the encrypted key and salt
    key_path = os.path.join("security", "biometric", "sovereign.key")
    os.makedirs(os.path.dirname(key_path), exist_ok=True)
    
    with open(key_path, 'wb') as f:
        f.write(salt + encrypted_key)
    
    # Clear variables
    del key_data
    del key_hash
    del encrypted_key
    del salt
    
    return key_path

if __name__ == "__main__":
    key_path = store_encrypted_key()
    print(f"Key securely stored at: {key_path}") 