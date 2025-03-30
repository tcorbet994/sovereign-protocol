from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import numpy as np
import torch
from typing import Dict, Any
import hashlib
import os

class SovereignProtocol:
    def __init__(self, owner_identity: str):
        self.owner_identity = owner_identity
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=4096,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()
        
    def sign_model_checkpoint(self, model_state: Dict[str, Any]) -> bytes:
        """Sign model checkpoint with owner's identity"""
        # Convert model state to bytes
        state_bytes = self._state_to_bytes(model_state)
        
        # Create signature
        signature = self.private_key.sign(
            state_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA3_512()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA3_512()
        )
        
        return signature
    
    def verify_ownership(self, model_state: Dict[str, Any], signature: bytes) -> bool:
        """Verify model ownership"""
        try:
            state_bytes = self._state_to_bytes(model_state)
            self.public_key.verify(
                signature,
                state_bytes,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA3_512()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA3_512()
            )
            return True
        except:
            return False
    
    def _state_to_bytes(self, model_state: Dict[str, Any]) -> bytes:
        """Convert model state to deterministic bytes"""
        state_hash = hashlib.sha3_512()
        
        # Sort keys for deterministic ordering
        for key in sorted(model_state.keys()):
            if isinstance(model_state[key], torch.Tensor):
                # Convert tensor to numpy array and then to bytes
                tensor_bytes = model_state[key].detach().cpu().numpy().tobytes()
                state_hash.update(tensor_bytes)
            elif isinstance(model_state[key], np.ndarray):
                state_hash.update(model_state[key].tobytes())
            else:
                state_hash.update(str(model_state[key]).encode())
        
        return state_hash.digest()
    
    def export_public_key(self) -> bytes:
        """Export public key for verification"""
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    
    def save_identity(self, path: str):
        """Save identity information securely"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            f.write(self.export_public_key()) 