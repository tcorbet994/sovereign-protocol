#!/usr/bin/env python3
import os
import sys
import platform
from pathlib import Path
import logging
from typing import Optional
import ctypes
import win32security
import win32api
import win32con
import win32process
import win32event
import win32service
import win32serviceutil
import win32timezone

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent.parent))

from autonomous_llm.security.initialize_owner import initialize_owner_identity

def is_admin() -> bool:
    """Check if running with administrator privileges"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def setup_logging() -> None:
    """Setup logging configuration"""
    try:
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # Set up file handler with proper permissions
        log_file = log_dir / "owner_init.log"
        if platform.system() == 'Windows':
            # Create file with restricted permissions
            handle = win32api.CreateFile(
                str(log_file),
                win32con.GENERIC_WRITE,
                win32con.FILE_SHARE_READ,
                None,
                win32con.CREATE_ALWAYS,
                win32con.FILE_ATTRIBUTE_NORMAL,
                None
            )
            win32api.CloseHandle(handle)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
    except Exception as e:
        print(f"Error setting up logging: {str(e)}")
        sys.exit(1)

def check_windows_requirements() -> bool:
    """Check if running on Windows and verify requirements"""
    if platform.system() == 'Windows':
        # Check for required Windows features
        required_modules = [
            'win32security',
            'win32api',
            'win32con',
            'win32process',
            'win32event',
            'win32service',
            'win32serviceutil',
            'win32timezone'
        ]
        
        missing_modules = []
        for module in required_modules:
            try:
                __import__(module)
            except ImportError:
                missing_modules.append(module)
        
        if missing_modules:
            print("Error: Required Windows modules not found:")
            for module in missing_modules:
                print(f"  - {module}")
            print("\nPlease install pywin32: pip install pywin32")
            return False
        
        # Check if running with admin privileges
        if not is_admin():
            print("Error: Administrator privileges required.")
            print("Please run this script as administrator.")
            return False
        
        # Check Windows version
        try:
            version = platform.win32_ver()
            if float(version[0]) < 10:
                print("Warning: Windows 10 or later is recommended")
        except:
            pass
        
        # Check if running in a secure environment
        try:
            # Check if running in a service
            if win32serviceutil.QueryServiceStatus(None)[1] == win32service.SERVICE_RUNNING:
                print("Warning: Running in a service context")
            
            # Check if running in a remote session
            if win32api.GetSystemMetrics(win32con.SM_REMOTESESSION):
                print("Warning: Running in a remote session")
        except:
            pass
    
    return True

def main():
    """Initialize the owner's biometric identity"""
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        print("\n=== Sovereign Control Protocol: Owner Identity Setup ===\n")
        print("This script will establish your biometric identity as the sole owner")
        print("of the autonomous LLM system. This is a critical security step that")
        print("should only be performed once during initial setup.\n")
        
        # Check Windows requirements if applicable
        if not check_windows_requirements():
            print("\nWindows-specific requirements not met.")
            print("Please address the issues above and try again.")
            sys.exit(1)
        
        # Check if owner identity already exists
        owner_key_path = Path("security/biometric/owner_key.enc")
        if owner_key_path.exists():
            print("WARNING: An owner identity already exists!")
            print("Running this script again will overwrite the existing identity.")
            print("Are you sure you want to continue?")
            print("Type 'OVERWRITE' to proceed:")
            
            confirmation = input().strip()
            if confirmation != "OVERWRITE":
                print("Initialization cancelled.")
                sys.exit(1)
        
        # Run initialization
        logger.info("Starting owner identity initialization")
        success = initialize_owner_identity()
        
        if success:
            logger.info("Owner identity successfully established")
            print("\nOwner identity successfully established.")
            print("You are now the sole authorized owner of the system.")
        else:
            logger.error("Failed to establish owner identity")
            print("\nFailed to establish owner identity.")
            print("Please check the error messages above and try again.")
            print("Detailed logs are available in logs/owner_init.log")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.warning("Initialization interrupted by user")
        print("\nInitialization cancelled by user.")
        sys.exit(1)
    except Exception as e:
        logger.exception("Unexpected error during initialization")
        print(f"\nUnexpected error: {str(e)}")
        print("Please check logs/owner_init.log for details.")
        sys.exit(1)

if __name__ == "__main__":
    main() 