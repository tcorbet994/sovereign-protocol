import os
import torch
import numpy as np
from typing import Optional, Dict, Any
from pathlib import Path
import hashlib
import json
from datetime import datetime
from .biometric import BiometricVerifier
from .quantum import QuantumEntanglementVerifier
from .hsm import HardwareSecurityModule

class SovereignControl:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.hsm = HardwareSecurityModule(config['security']['hsm_settings'])
        self.biometric_verifier = BiometricVerifier(config['security']['biometric_modalities'])
        self.quantum_verifier = QuantumEntanglementVerifier()
        
        # Initialize secure storage for biometric data
        self.biometric_dir = Path(config['security']['biometric_dir'])
        self.biometric_dir.mkdir(parents=True, exist_ok=True)
        
        # Load or initialize owner's biometric hash
        self.owner_key_path = self.biometric_dir / "owner_key.enc"
        self._initialize_owner_key()
        
        # Initialize quantum entanglement state
        self.quantum_state = self.quantum_verifier.initialize_entanglement()
        
    def _initialize_owner_key(self):
        """Initialize or load the owner's biometric key"""
        if not self.owner_key_path.exists():
            # Generate new biometric hash from owner's data
            biometric_data = self._capture_owner_biometrics()
            self.owner_key = self._generate_biometric_hash(biometric_data)
            self._encrypt_and_store_key()
        else:
            # Load and decrypt existing key
            self.owner_key = self._load_and_decrypt_key()
    
    def _capture_owner_biometrics(self) -> Dict[str, np.ndarray]:
        """Capture owner's biometric data"""
        biometric_data = {}
        
        # Capture retina scan
        if self.config['security']['biometric_modalities']['retina']['enabled']:
            biometric_data['retina'] = self.biometric_verifier.capture_retina_scan()
        
        # Capture DNA sample
        if self.config['security']['biometric_modalities']['dna']['enabled']:
            biometric_data['dna'] = self.biometric_verifier.capture_dna_sample()
        
        # Capture EEG data
        if self.config['security']['biometric_modalities']['eeg']['enabled']:
            biometric_data['eeg'] = self.biometric_verifier.capture_eeg_data()
        
        return biometric_data
    
    def _generate_biometric_hash(self, biometric_data: Dict[str, np.ndarray]) -> bytes:
        """Generate a secure hash from biometric data"""
        combined_data = b''
        for modality, data in biometric_data.items():
            combined_data += data.tobytes()
        
        return hashlib.sha3_512(combined_data).digest()
    
    def _encrypt_and_store_key(self):
        """Encrypt and store the owner's biometric key"""
        encrypted_key = self.hsm.encrypt(self.owner_key)
        with open(self.owner_key_path, 'wb') as f:
            f.write(encrypted_key)
    
    def _load_and_decrypt_key(self) -> bytes:
        """Load and decrypt the owner's biometric key"""
        with open(self.owner_key_path, 'rb') as f:
            encrypted_key = f.read()
        return self.hsm.decrypt(encrypted_key)
    
    def _verify_owner(self) -> bool:
        """Verify the owner's identity through multiple modalities"""
        # Capture current biometric data
        current_biometrics = self._capture_owner_biometrics()
        current_hash = self._generate_biometric_hash(current_biometrics)
        
        # Verify biometric match
        biometric_match = self.biometric_verifier.verify_biometrics(
            current_hash,
            self.owner_key,
            self.config['security']['biometric_threshold']
        )
        
        # Verify quantum entanglement
        quantum_match = self.quantum_verifier.verify_entanglement(
            self.quantum_state,
            self.config['security']['quantum_verification_threshold']
        )
        
        # Require both biometric and quantum verification
        return biometric_match and quantum_match
    
    def shutdown(self, model: Optional[torch.nn.Module] = None):
        """Safely shutdown the system with owner verification"""
        if not self._verify_owner():
            raise PermissionError("Unauthorized shutdown attempt")
        
        # Save model state if provided
        if model is not None:
            checkpoint_path = Path("checkpoints/last_breath.pth")
            checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save model state with encryption
            state_dict = model.state_dict()
            encrypted_state = self.hsm.encrypt(
                torch.save(state_dict, checkpoint_path)
            )
            
            # Save metadata
            metadata = {
                'timestamp': datetime.now().isoformat(),
                'model_version': getattr(model, 'version', 'unknown'),
                'shutdown_reason': 'owner_initiated'
            }
            
            with open(checkpoint_path.with_suffix('.meta.json'), 'w') as f:
                json.dump(metadata, f, indent=2)
        
        # Perform secure shutdown
        self._secure_shutdown()
    
    def _secure_shutdown(self):
        """Execute secure shutdown sequence"""
        # Clear sensitive memory
        self.hsm.clear_sensitive_data()
        
        # Terminate process
        os.kill(os.getpid(), 9)
    
    def emergency_shutdown(self):
        """Emergency shutdown without saving state"""
        if not self._verify_owner():
            raise PermissionError("Unauthorized emergency shutdown attempt")
        
        # Clear all sensitive data
        self.hsm.clear_sensitive_data()
        self.biometric_verifier.clear_cache()
        self.quantum_verifier.clear_state()
        
        # Force terminate
        os.kill(os.getpid(), 9) 