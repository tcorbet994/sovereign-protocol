# Set up Sovereign Control Protocol
Write-Host "Setting up Sovereign Control Protocol..." -ForegroundColor Green

# Remove existing venv if it exists
if (Test-Path "venv") {
    Write-Host "Removing existing virtual environment..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force venv
}

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
try {
    python -m venv venv
    if (-not $?) { throw "Failed to create virtual environment" }
} catch {
    Write-Host "Error creating virtual environment: $_" -ForegroundColor Red
    exit 1
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
try {
    & .\venv\Scripts\Activate.ps1
    if (-not $?) { throw "Failed to activate virtual environment" }
} catch {
    Write-Host "Error activating virtual environment: $_" -ForegroundColor Red
    exit 1
}

# Install requirements
Write-Host "Installing requirements..." -ForegroundColor Yellow
try {
    pip install -r requirements.txt
    if (-not $?) { throw "Failed to install requirements" }
} catch {
    Write-Host "Error installing requirements: $_" -ForegroundColor Red
    exit 1
}

# Run the initialization script
Write-Host "Running initialization script..." -ForegroundColor Yellow
try {
    python initialize_owner.py
    if (-not $?) { throw "Failed to run initialization script" }
} catch {
    Write-Host "Error running initialization script: $_" -ForegroundColor Red
    exit 1
}

# Start the interface
Write-Host "Starting the interface..." -ForegroundColor Yellow
try {
    python sovereign_interface.py
    if (-not $?) { throw "Failed to start interface" }
} catch {
    Write-Host "Error starting interface: $_" -ForegroundColor Red
    exit 1
}

# Deactivate virtual environment
deactivate

Write-Host "Setup complete!" -ForegroundColor Green 