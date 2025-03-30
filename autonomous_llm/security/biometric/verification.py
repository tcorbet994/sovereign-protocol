import numpy as np
from typing import Dict, Any, Optional
import hashlib
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

class BiometricVerification:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.biometric_data_dir = os.path.join(config['security']['biometric_dir'], 'data')
        os.makedirs(self.biometric_data_dir, exist_ok=True)
        
    def register_biometric(self, user_id: str, biometric_data: Dict[str, Any]) -> bool:
        """Register new biometric data for a user"""
        # Hash and salt the biometric data
        hashed_data = self._hash_biometric_data(biometric_data)
        
        # Store the hashed data
        user_file = os.path.join(self.biometric_data_dir, f"{user_id}.bio")
        with open(user_file, 'wb') as f:
            f.write(hashed_data)
        
        return True
    
    def verify_biometric(self, user_id: str, biometric_data: Dict[str, Any]) -> bool:
        """Verify user's biometric data"""
        user_file = os.path.join(self.biometric_data_dir, f"{user_id}.bio")
        
        if not os.path.exists(user_file):
            return False
        
        # Hash the provided biometric data
        hashed_input = self._hash_biometric_data(biometric_data)
        
        # Compare with stored data
        with open(user_file, 'rb') as f:
            stored_hash = f.read()
        
        return self._compare_hashes(hashed_input, stored_hash)
    
    def _hash_biometric_data(self, biometric_data: Dict[str, Any]) -> bytes:
        """Hash biometric data with salt"""
        # Create a unique salt for this user
        salt = os.urandom(16)
        
        # Convert biometric data to bytes
        data_bytes = self._biometric_to_bytes(biometric_data)
        
        # Use PBKDF2 for key derivation
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA3_512(),
            length=64,
            salt=salt,
            iterations=100000,
        )
        
        # Generate key
        key = kdf.derive(data_bytes)
        
        # Combine salt and key
        return salt + key
    
    def _biometric_to_bytes(self, biometric_data: Dict[str, Any]) -> bytes:
        """Convert biometric data to bytes"""
        # Sort keys for deterministic ordering
        sorted_data = {k: biometric_data[k] for k in sorted(biometric_data.keys())}
        
        # Convert to string and then to bytes
        data_str = str(sorted_data)
        return data_str.encode()
    
    def _compare_hashes(self, hash1: bytes, hash2: bytes) -> bool:
        """Compare two hashes with timing-safe comparison"""
        if len(hash1) != len(hash2):
            return False
        
        result = 0
        for x, y in zip(hash1, hash2):
            result |= x ^ y
        
        return result == 0
    
    def generate_biometric_key(self, user_id: str, biometric_data: Dict[str, Any]) -> bytes:
        """Generate a cryptographic key from biometric data"""
        # Hash biometric data
        hashed_data = self._hash_biometric_data(biometric_data)
        
        # Use PBKDF2 to generate a key
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA3_512(),
            length=32,
            salt=hashed_data[:16],
            iterations=100000,
        )
        
        # Generate key
        key = kdf.derive(hashed_data[16:])
        
        return key 