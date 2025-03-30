import sys
import os
from pathlib import Path

def check_environment():
    """Check if the Python environment is properly set up"""
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Available Python packages:")
    try:
        import pkg_resources
        for package in pkg_resources.working_set:
            print(f"- {package.key} {package.version}")
    except ImportError:
        print("Could not list installed packages")
    
    # Check if we can create directories
    try:
        test_dir = Path("test_dir")
        test_dir.mkdir(exist_ok=True)
        test_dir.rmdir()
        print("\nDirectory creation test: PASSED")
    except Exception as e:
        print(f"\nDirectory creation test: FAILED - {str(e)}")
    
    # Check if we can write files
    try:
        test_file = Path("test_file.txt")
        test_file.write_text("test")
        test_file.unlink()
        print("File writing test: PASSED")
    except Exception as e:
        print(f"File writing test: FAILED - {str(e)}")

if __name__ == "__main__":
    check_environment() 