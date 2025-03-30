@echo off
echo Setting up Sovereign Control Protocol...

:: Install required packages
pip install numpy cryptography

:: Run the initialization script
python simple_init.py

pause 