import os
import hashlib
import hmac
from typing import Dict, Any, Optional
from pathlib import Path
import json
from datetime import datetime, timedelta
import uuid

class HardwareSecurityModule:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.hsm_dir = Path(config.get('hsm_dir', 'security/hsm'))
        self.hsm_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize master key
        self.master_key = self._initialize_master_key()
        
        # Initialize key rotation schedule
        self.last_rotation = datetime.now()
        self.rotation_period = timedelta(days=config.get('master_key_rotation_days', 30))
        
        # Initialize system entropy
        self.system_entropy = self._generate_system_entropy()
    
    def _initialize_master_key(self) -> bytes:
        """Initialize or load master key"""
        master_key_path = self.hsm_dir / "master_key.enc"
        
        if not master_key_path.exists():
            # Generate new master key
            master_key = os.urandom(32)
            self._save_master_key(master_key)
            return master_key
        else:
            # Load existing master key
            return self._load_master_key()
    
    def _save_master_key(self, key: bytes):
        """Save master key with encryption"""
        # In a real implementation, this would use hardware encryption
        # For now, we'll use a simplified encryption scheme
        salt = os.urandom(16)
        key_hash = hashlib.pbkdf2_hmac(
            'sha256',
            key,
            salt,
            100000
        )
        
        with open(self.hsm_dir / "master_key.enc", 'wb') as f:
            f.write(salt + key_hash)
    
    def _load_master_key(self) -> bytes:
        """Load master key from storage"""
        with open(self.hsm_dir / "master_key.enc", 'rb') as f:
            data = f.read()
            salt = data[:16]
            key_hash = data[16:]
            
            # In a real implementation, this would use hardware decryption
            # For now, we'll use a simplified decryption scheme
            return key_hash
    
    def _generate_system_entropy(self) -> bytes:
        """Generate system entropy from hardware sources"""
        entropy_sources = self.config.get('system_entropy_sources', [])
        entropy_data = b''
        
        for source in entropy_sources:
            if source == 'cpu_id':
                entropy_data += self._get_cpu_id().encode()
            elif source == 'disk_id':
                entropy_data += self._get_disk_id().encode()
            elif source == 'mac_address':
                entropy_data += self._get_mac_address().encode()
            elif source == 'hardware_tpm':
                entropy_data += self._get_tpm_entropy()
        
        return hashlib.sha3_512(entropy_data).digest()
    
    def _get_cpu_id(self) -> str:
        """Get CPU ID"""
        # In a real implementation, this would read from CPU registers
        return str(uuid.uuid4())  # Placeholder
    
    def _get_disk_id(self) -> str:
        """Get disk ID"""
        # In a real implementation, this would read from disk firmware
        return str(uuid.uuid4())  # Placeholder
    
    def _get_mac_address(self) -> str:
        """Get MAC address"""
        # In a real implementation, this would read from network interface
        return str(uuid.uuid4())  # Placeholder
    
    def _get_tpm_entropy(self) -> bytes:
        """Get entropy from TPM"""
        # In a real implementation, this would interface with TPM
        return os.urandom(32)  # Placeholder
    
    def encrypt(self, data: bytes) -> bytes:
        """Encrypt data using master key"""
        # Check if key rotation is needed
        self._check_key_rotation()
        
        # In a real implementation, this would use hardware encryption
        # For now, we'll use a simplified encryption scheme
        iv = os.urandom(16)
        key = hmac.new(self.master_key, self.system_entropy, 'sha256').digest()
        
        # Simple XOR encryption (placeholder)
        encrypted = bytes(a ^ b for a, b in zip(data, key))
        
        return iv + encrypted
    
    def decrypt(self, data: bytes) -> bytes:
        """Decrypt data using master key"""
        # In a real implementation, this would use hardware decryption
        # For now, we'll use a simplified decryption scheme
        iv = data[:16]
        encrypted = data[16:]
        key = hmac.new(self.master_key, self.system_entropy, 'sha256').digest()
        
        # Simple XOR decryption (placeholder)
        return bytes(a ^ b for a, b in zip(encrypted, key))
    
    def _check_key_rotation(self):
        """Check if master key needs rotation"""
        if datetime.now() - self.last_rotation > self.rotation_period:
            self._rotate_master_key()
    
    def _rotate_master_key(self):
        """Rotate master key"""
        new_key = os.urandom(32)
        self._save_master_key(new_key)
        self.master_key = new_key
        self.last_rotation = datetime.now()
    
    def clear_sensitive_data(self):
        """Clear sensitive data from memory"""
        # Overwrite sensitive data with random values
        self.master_key = os.urandom(32)
        self.system_entropy = os.urandom(32) 