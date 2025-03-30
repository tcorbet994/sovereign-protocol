@echo off
echo Setting up Sovereign Control Protocol...

:: Create virtual environment
python -m venv venv

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Install requirements
pip install numpy cryptography python-dotenv

:: Run the initialization script
python run_owner_init.py

:: Deactivate virtual environment
deactivate

pause 