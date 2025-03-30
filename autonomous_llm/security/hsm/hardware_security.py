from typing import Dict, Any, Optional
import os
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import json

class HardwareSecurityModule:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.hsm_dir = os.path.join(config['security']['hsm_dir'], 'secure')
        os.makedirs(self.hsm_dir, exist_ok=True)
        
        # Initialize HSM with master key
        self.master_key = self._initialize_master_key()
        
    def _initialize_master_key(self) -> bytes:
        """Initialize or load master key"""
        master_key_path = os.path.join(self.hsm_dir, 'master.key')
        
        if os.path.exists(master_key_path):
            # Load existing master key
            with open(master_key_path, 'rb') as f:
                encrypted_key = f.read()
            return self._decrypt_master_key(encrypted_key)
        else:
            # Generate new master key
            master_key = os.urandom(32)
            encrypted_key = self._encrypt_master_key(master_key)
            with open(master_key_path, 'wb') as f:
                f.write(encrypted_key)
            return master_key
    
    def _encrypt_master_key(self, key: bytes) -> bytes:
        """Encrypt master key using system-specific entropy"""
        # Use system-specific entropy for encryption
        iv = os.urandom(16)
        cipher = Cipher(
            algorithms.AES(self._get_system_entropy()),
            modes.CBC(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        
        # Pad key to block size
        padded_key = key + b'\0' * (16 - (len(key) % 16))
        
        # Encrypt
        encrypted = encryptor.update(padded_key) + encryptor.finalize()
        
        # Combine IV and encrypted data
        return iv + encrypted
    
    def _decrypt_master_key(self, encrypted_data: bytes) -> bytes:
        """Decrypt master key"""
        # Extract IV and encrypted data
        iv = encrypted_data[:16]
        encrypted = encrypted_data[16:]
        
        # Create cipher
        cipher = Cipher(
            algorithms.AES(self._get_system_entropy()),
            modes.CBC(iv),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        
        # Decrypt
        decrypted = decryptor.update(encrypted) + decryptor.finalize()
        
        # Remove padding
        return decrypted.rstrip(b'\0')
    
    def _get_system_entropy(self) -> bytes:
        """Get system-specific entropy for key derivation"""
        # Collect system-specific information
        system_info = {
            'cpu_id': self._get_cpu_id(),
            'disk_id': self._get_disk_id(),
            'mac_address': self._get_mac_address()
        }
        
        # Convert to bytes and hash
        info_bytes = json.dumps(system_info, sort_keys=True).encode()
        return hashlib.sha3_512(info_bytes).digest()[:32]
    
    def _get_cpu_id(self) -> str:
        """Get CPU ID (platform-specific)"""
        # Implement platform-specific CPU ID retrieval
        return "PLACEHOLDER_CPU_ID"
    
    def _get_disk_id(self) -> str:
        """Get disk ID (platform-specific)"""
        # Implement platform-specific disk ID retrieval
        return "PLACEHOLDER_DISK_ID"
    
    def _get_mac_address(self) -> str:
        """Get MAC address (platform-specific)"""
        # Implement platform-specific MAC address retrieval
        return "PLACEHOLDER_MAC_ADDRESS"
    
    def generate_key_pair(self, user_id: str) -> Dict[str, bytes]:
        """Generate a new key pair for a user"""
        # Generate private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=4096,
            backend=default_backend()
        )
        
        # Get public key
        public_key = private_key.public_key()
        
        # Serialize keys
        private_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        public_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        # Encrypt private key with master key
        encrypted_private = self._encrypt_with_master_key(private_bytes)
        
        # Save keys
        self._save_user_keys(user_id, encrypted_private, public_bytes)
        
        return {
            'private_key': private_bytes,
            'public_key': public_bytes
        }
    
    def _encrypt_with_master_key(self, data: bytes) -> bytes:
        """Encrypt data using master key"""
        iv = os.urandom(16)
        cipher = Cipher(
            algorithms.AES(self.master_key),
            modes.CBC(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        
        # Pad data
        padded_data = data + b'\0' * (16 - (len(data) % 16))
        
        # Encrypt
        encrypted = encryptor.update(padded_data) + encryptor.finalize()
        
        return iv + encrypted
    
    def _decrypt_with_master_key(self, encrypted_data: bytes) -> bytes:
        """Decrypt data using master key"""
        iv = encrypted_data[:16]
        encrypted = encrypted_data[16:]
        
        cipher = Cipher(
            algorithms.AES(self.master_key),
            modes.CBC(iv),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        
        decrypted = decryptor.update(encrypted) + decryptor.finalize()
        return decrypted.rstrip(b'\0')
    
    def _save_user_keys(self, user_id: str, encrypted_private: bytes, public: bytes):
        """Save user's encrypted keys"""
        user_dir = os.path.join(self.hsm_dir, user_id)
        os.makedirs(user_dir, exist_ok=True)
        
        with open(os.path.join(user_dir, 'private.key'), 'wb') as f:
            f.write(encrypted_private)
        
        with open(os.path.join(user_dir, 'public.key'), 'wb') as f:
            f.write(public)
    
    def load_user_keys(self, user_id: str) -> Optional[Dict[str, bytes]]:
        """Load user's keys"""
        user_dir = os.path.join(self.hsm_dir, user_id)
        
        if not os.path.exists(user_dir):
            return None
        
        try:
            with open(os.path.join(user_dir, 'private.key'), 'rb') as f:
                encrypted_private = f.read()
            
            with open(os.path.join(user_dir, 'public.key'), 'rb') as f:
                public = f.read()
            
            private = self._decrypt_with_master_key(encrypted_private)
            
            return {
                'private_key': private,
                'public_key': public
            }
        except:
            return None
    
    def sign_data(self, user_id: str, data: bytes) -> Optional[bytes]:
        """Sign data using user's private key"""
        keys = self.load_user_keys(user_id)
        if not keys:
            return None
        
        try:
            private_key = serialization.load_pem_private_key(
                keys['private_key'],
                password=None,
                backend=default_backend()
            )
            
            signature = private_key.sign(
                data,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA3_512()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA3_512()
            )
            
            return signature
        except:
            return None
    
    def verify_signature(self, user_id: str, data: bytes, signature: bytes) -> bool:
        """Verify signature using user's public key"""
        keys = self.load_user_keys(user_id)
        if not keys:
            return False
        
        try:
            public_key = serialization.load_pem_public_key(
                keys['public_key'],
                backend=default_backend()
            )
            
            public_key.verify(
                signature,
                data,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA3_512()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA3_512()
            )
            return True
        except:
            return False 