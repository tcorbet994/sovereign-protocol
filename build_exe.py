import PyInstaller.__main__
import os

# Get the absolute path to the icon file
current_dir = os.path.dirname(os.path.abspath(__file__))

PyInstaller.__main__.run([
    'run.py',  # Your main script
    '--name=SovereignProtocol',  # Name of the executable
    '--onefile',  # Create a single executable file
    '--noconsole',  # Don't show console window
    '--add-data=static;static',  # Include static files
    '--add-data=config;config',  # Include config files
    '--hidden-import=uvicorn.logging',
    '--hidden-import=uvicorn.protocols',
    '--hidden-import=fastapi',
]) 