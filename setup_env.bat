@echo off
echo Setting up Python environment...

:: Create virtual environment
python -m venv venv

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Install required packages
pip install numpy cryptography

:: Run the initialization script
python simple_uuid_init.py

:: Deactivate virtual environment
deactivate

pause 