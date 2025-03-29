# Set up Sovereign Control Protocol
Write-Host "Setting up Sovereign Control Protocol..." -ForegroundColor Green

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
python -m venv venv

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Install requirements
Write-Host "Installing requirements..." -ForegroundColor Yellow
pip install numpy cryptography python-dotenv

# Run the initialization script
Write-Host "Running initialization script..." -ForegroundColor Yellow
python run_owner_init.py

# Deactivate virtual environment
deactivate

Write-Host "Setup complete!" -ForegroundColor Green 