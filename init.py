import os
import sys
import json
import shutil
from pathlib import Path

def create_directories():
    """Create necessary directories for the project."""
    directories = [
        "config",
        "security/biometric",
        "security/biometric/cache",
        "security/quantum",
        "security/quantum/state",
        "logs",
        "static"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {directory}")

def create_default_config():
    """Create default configuration file."""
    config = {
        "security_level": "MAXIMUM",
        "quantum_state": "STABLE",
        "interface_port": 8000,
        "websocket_port": 8001,
        "log_level": "INFO"
    }
    
    config_path = Path("config/default_config.json")
    with open(config_path, "w") as f:
        json.dump(config, f, indent=4)
    print(f"Created default configuration: {config_path}")

def setup_environment():
    """Set up the Python environment."""
    try:
        import pip
    except ImportError:
        print("pip is not installed. Please install pip first.")
        sys.exit(1)
    
    # Install required packages
    os.system(f"{sys.executable} -m pip install -e .[dev]")
    print("Installed required packages")

def main():
    """Main initialization function."""
    print("=== Sovereign Control Protocol Initialization ===")
    
    # Create directories
    create_directories()
    
    # Create default configuration
    create_default_config()
    
    # Set up environment
    setup_environment()
    
    print("\nInitialization completed successfully!")
    print("\nNext steps:")
    print("1. Run 'python -m sovereign_control' to start the interface")
    print("2. Access the web interface at http://localhost:8000")
    print("3. Follow the security setup prompts")

if __name__ == "__main__":
    main() 