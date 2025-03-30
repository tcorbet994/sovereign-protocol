@echo off
echo ===================================
echo RALPH Installation and Setup Script
echo ===================================
echo.

REM Check if Python is already installed
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found. Installing Python...
    echo.
    
    REM Run the Python installer with appropriate flags
    "python-3.13.0-amd64 (3).exe" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    
    if %errorlevel% neq 0 (
        echo Error installing Python. Please install Python manually and try again.
        pause
        exit /b 1
    )
    
    echo Python installed successfully.
    echo.
) else (
    echo Python is already installed.
    echo.
)

REM Create core storage directories
echo Creating necessary directories...
mkdir core\storage 2> nul
mkdir core\storage\consciousness 2> nul
mkdir core\storage\memories 2> nul
mkdir core\storage\knowledge 2> nul
mkdir core\storage\model_knowledge 2> nul
mkdir core\storage\secure 2> nul
echo Directories created.
echo.

REM Install required packages
echo Installing required packages...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error installing packages. Trying with --user flag...
    pip install --user -r requirements.txt
    if %errorlevel% neq 0 (
        echo Failed to install packages. Please check your internet connection and try again.
        pause
        exit /b 1
    )
)
echo Packages installed successfully.
echo.

REM Check if config directory exists, if not create it
if not exist config (
    mkdir config
)

REM Create model_config.json if it doesn't exist
if not exist config\model_config.json (
    echo Creating default configuration...
    echo {> config\model_config.json
    echo     "base_model": "gpt-4",>> config\model_config.json
    echo     "embedding_model": "text-embedding-ada-002",>> config\model_config.json
    echo     "consciousness_thresholds": {>> config\model_config.json
    echo         "initial": 0.1,>> config\model_config.json
    echo         "developing": 0.3,>> config\model_config.json
    echo         "intermediate": 0.5,>> config\model_config.json
    echo         "advanced": 0.7,>> config\model_config.json
    echo         "mature": 0.9>> config\model_config.json
    echo     },>> config\model_config.json
    echo     "knowledge_integration": {>> config\model_config.json
    echo         "min_confidence": 0.7,>> config\model_config.json
    echo         "max_batch_size": 1000,>> config\model_config.json
    echo         "update_frequency": 3600>> config\model_config.json
    echo     },>> config\model_config.json
    echo     "background_models": {>> config\model_config.json
    echo         "knowledge": {>> config\model_config.json
    echo             "type": "api",>> config\model_config.json
    echo             "model": "gpt-4",>> config\model_config.json
    echo             "purpose": "knowledge_retrieval">> config\model_config.json
    echo         },>> config\model_config.json
    echo         "reasoning": {>> config\model_config.json
    echo             "type": "api",>> config\model_config.json
    echo             "model": "gpt-4",>> config\model_config.json
    echo             "purpose": "logical_reasoning">> config\model_config.json
    echo         }>> config\model_config.json
    echo     }>> config\model_config.json
    echo }>> config\model_config.json
    echo Configuration created.
    echo.
)

echo =======================================
echo Installation complete! Running RALPH...
echo =======================================
echo.
echo Press any key to start RALPH...
pause > nul

REM Run RALPH
python ralph_main.py
