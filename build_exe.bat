@echo off
echo Building Sovereign LLM Executable...

REM Activate virtual environment if it exists
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
)

REM Install requirements
pip install -r requirements.txt

REM Build the executable
pyinstaller --clean sovereign_llm.spec

echo Build complete!
echo Executable can be found in the dist folder.
pause 