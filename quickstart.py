#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required")
        sys.exit(1)

def check_git():
    """Check if Git is installed."""
    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True)
    except subprocess.CalledProcessError:
        print("Error: Git is not installed. Please install Git first.")
        sys.exit(1)

def setup_repository():
    """Set up the Git repository if not already initialized."""
    if not Path(".git").exists():
        print("Initializing Git repository...")
        subprocess.run(["git", "init"], check=True)
        print("Git repository initialized.")

def main():
    """Quickstart script for the Sovereign Control Protocol."""
    print("=== Sovereign Control Protocol Quickstart ===")
    
    # Check prerequisites
    check_python_version()
    check_git()
    
    # Set up repository
    setup_repository()
    
    # Run initialization
    print("\nRunning initialization...")
    subprocess.run([sys.executable, "init.py"], check=True)
    
    print("\n=== Quickstart Complete! ===")
    print("\nTo start the interface, run:")
    print("python -m sovereign_control")
    print("\nTo access the web interface, open:")
    print("http://localhost:8000")

if __name__ == "__main__":
    main() 