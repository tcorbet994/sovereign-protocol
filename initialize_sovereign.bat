@echo off
echo Setting up Sovereign Control Protocol...

:: First, store the secure key
python secure_key.py

:: Then run the initialization
python verify_and_run.py

pause 