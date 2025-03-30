import os
import sys
import platform
from pathlib import Path
import json
from typing import Dict, Any, Optional
import numpy as np
from god_key import SovereignControl
from .biometric import BiometricVerifier
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import base64

def validate_config(config: Dict[str, Any]) -> bool:
    """Validate the configuration file"""
    required_sections = ['security', 'security.biometric_modalities']
    for section in required_sections:
        current = config
        for key in section.split('.'):
            if key not in current:
                print(f"Error: Missing required configuration section '{section}'")
                return False
            current = current[key]
    return True

def check_environment() -> bool:
    """Check if the environment is suitable for initialization"""
    try:
        # Windows-specific checks
        if platform.system() == 'Windows':
            try:
                import win32security
                import win32api
                import win32con
                if not win32security.IsUserAnAdmin():
                    print("Warning: Not running with administrator privileges")
            except ImportError:
                print("Warning: Windows security modules not available")
        else:
            # Unix-specific checks
            if os.geteuid() == 0:
                print("Warning: Running as root is not recommended for security reasons")
        
        # Check if running in a secure environment
        if os.environ.get('PYTHONUNBUFFERED') != '1':
            print("Warning: PYTHONUNBUFFERED not set, which may affect security logging")
        
        # Check if running in a virtual environment
        if not hasattr(sys, 'real_prefix') and not hasattr(sys, 'base_prefix'):
            print("Warning: Not running in a virtual environment")
        
        return True
    except Exception as e:
        print(f"Error checking environment: {str(e)}")
        return False

def set_directory_permissions(directory: Path) -> bool:
    """Set directory permissions securely"""
    try:
        if platform.system() == 'Windows':
            import win32security
            import win32con
            import win32api
            
            # Get current user SID
            user_sid = win32security.GetTokenInformation(
                win32security.OpenProcessToken(win32api.GetCurrentProcess(), win32con.TOKEN_QUERY),
                win32security.TokenUser
            )[0]
            
            # Set directory security
            sd = win32security.GetFileSecurity(
                str(directory),
                win32security.DACL_SECURITY_INFORMATION
            )
            dacl = sd.GetSecurityDescriptorDacl()
            
            # Remove all existing ACEs
            while dacl.GetAceCount() > 0:
                dacl.DeleteAce(0)
            
            # Add new ACE for current user only
            dacl.AddAccessAllowedAce(
                win32security.ACL_REVISION,
                win32con.GENERIC_ALL,
                user_sid
            )
            
            sd.SetSecurityDescriptorDacl(1, dacl, 0)
            win32security.SetFileSecurity(
                str(directory),
                win32security.DACL_SECURITY_INFORMATION,
                sd
            )
        else:
            # Unix permissions
            os.chmod(directory, 0o700)
        
        return True
    except Exception as e:
        print(f"Error setting directory permissions: {str(e)}")
        return False

def initialize_owner_identity(config_path: str = "config/default_config.json") -> bool:
    """
    Initialize the owner's biometric identity and create the God Key.
    This should only be run once during initial setup.
    """
    try:
        # Check environment
        if not check_environment():
            print("Environment check failed. Please address the warnings above.")
            return False
        
        # Load and validate configuration
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
        except FileNotFoundError:
            print(f"Error: Configuration file not found at {config_path}")
            return False
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in configuration file {config_path}")
            return False
        
        if not validate_config(config):
            return False
        
        # Create security directories with proper permissions
        security_dir = Path("security")
        biometric_dir = security_dir / "biometric"
        hsm_dir = security_dir / "hsm"
        quantum_dir = security_dir / "quantum"
        
        for directory in [security_dir, biometric_dir, hsm_dir, quantum_dir]:
            try:
                directory.mkdir(parents=True, exist_ok=True)
                if not set_directory_permissions(directory):
                    return False
            except Exception as e:
                print(f"Error creating directory {directory}: {str(e)}")
                return False
        
        # Initialize biometric verifier
        try:
            biometric_verifier = BiometricVerifier(config['security']['biometric_modalities'])
        except Exception as e:
            print(f"Error initializing biometric verifier: {str(e)}")
            return False
        
        print("=== Sovereign Control Protocol: Owner Identity Initialization ===\n")

        try:
            print("This process will establish your biometric identity as the sole owner.")
            print("This action cannot be undone. Are you sure you want to continue?")
            print("Type 'CONFIRM' to proceed:")
            
            confirmation = input().strip()
            if confirmation != "CONFIRM":
                print("Initialization cancelled.")
                exit()

            print("\nInitializing Sovereign Control...\n")
            
            # Add debug prints
            print("Debug: Importing required modules...")
            from god_key import SovereignControl
            print("Debug: SovereignControl imported successfully")
            
            # Initialize with debug
            print("Debug: Creating SovereignControl instance...")
            control = SovereignControl()
            print("Debug: Instance created successfully")
            
            # Continue with initialization
            print("Debug: Starting initialization process...")
            control.initialize_owner()
            print("Debug: Initialization completed")

        except Exception as e:
            print(f"\nUnexpected error during initialization:")
            print(f"Error details: {str(e)}")
            import traceback
            traceback.print_exc()
        
        # Initialize quantum entanglement
        print("\nInitializing quantum entanglement...")
        try:
            control.quantum_state = control.quantum_verifier.initialize_entanglement()
        except Exception as e:
            print(f"Error initializing quantum entanglement: {str(e)}")
            return False
        
        print("\n=== Owner Identity Successfully Established ===\n")
        print("Your biometric identity has been securely stored.")
        print("You are now the sole authorized owner of this system.")
        print("\nSecurity measures in place:")
        print(f"- Biometric verification: {len(control.biometric_data)} modalities")
        print("- Quantum entanglement verification")
        print("- Hardware security module")
        print("- Encrypted key storage")
        
        return True
        
    except Exception as e:
        print(f"\nDetailed error: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        traceback.print_exc()
        return False

def _verify_owner(self) -> bool:
    # Capture current biometric data
    current_biometrics = self._capture_owner_biometrics()
    current_hash = self._generate_biometric_hash(current_biometrics)
    
    # Verify biometric match
    biometric_match = self._verify_biometric_hash(
        current_hash,
        self.owner_key,
        self.config['security']['biometric_threshold']
    )

def verify_entanglement(self, state: Dict[str, Any], threshold: float) -> bool:
    if self.entanglement_state is None:
        return False
    
    fidelity = self._calculate_entanglement_fidelity(
        state['entanglement_matrix'],
        self.entanglement_state['entanglement_matrix']
    )

def _encrypt_and_store_key(self):
    # Generate a key from system entropy
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(os.urandom(32)))

if __name__ == "__main__":
    success = initialize_owner_identity()
    sys.exit(0 if success else 1) 