@echo off
echo Checking Python installation...

:: Check Python version
python --version

:: Check pip version
pip --version

:: Check if we can run Python
python -c "print('Python is working!')"

pause 