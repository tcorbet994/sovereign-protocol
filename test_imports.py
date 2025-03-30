# Test all critical imports
try:
    import numpy
    print("✓ numpy")
    
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    print("✓ cryptography")
    
    import win32security
    import win32api
    import win32con
    print("✓ pywin32")
    
    import pytest
    print("✓ pytest")
    
    import psutil
    print("✓ psutil")
    
    import requests
    print("✓ requests")
    
    import websockets
    print("✓ websockets")
    
    import neurokit2
    print("✓ neurokit2")
    
    import fastapi
    print("✓ fastapi")
    
    import uvicorn
    print("✓ uvicorn")
    
except ImportError as e:
    print(f"❌ Error: {e}") 