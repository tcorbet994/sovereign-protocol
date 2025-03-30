@echo off
echo Starting Sovereign Control Protocol Interface...

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Run the interface
python sovereign_interface.py

:: Deactivate virtual environment
deactivate

pause 