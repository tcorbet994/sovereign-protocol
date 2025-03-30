@echo off
echo Installing RALPH...
echo ==================

:: Check Python installation
python --version
if errorlevel 1 (
    echo Python not found! Please install Python 3.10 or higher.
    pause
    exit /b 1
)

:: Create virtual environment
echo Creating virtual environment...
python -m venv .venv

:: Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

:: Install requirements
echo Installing required packages...
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

:: Build the executable
echo Building RALPH...
pyinstaller --clean ^
    --add-data "config;config" ^
    --add-data "static;static" ^
    --add-data "models;models" ^
    --add-data "security;security" ^
    --add-data "sovereign_control;sovereign_control" ^
    --name RALPH ^
    sovereign_llm.py

:: Create launcher
echo Creating launcher...
echo @echo off > launch_RALPH.bat
echo echo Starting RALPH... >> launch_RALPH.bat
echo start "" "dist\RALPH.exe" >> launch_RALPH.bat

echo Installation complete!
echo You can find RALPH.exe in the dist folder
echo Use launch_RALPH.bat to start RALPH
pause