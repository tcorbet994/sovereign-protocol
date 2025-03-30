Write-Host "Setting up Sovereign Control Protocol..." -ForegroundColor Green

# Get Python path
$pythonPath = (Get-Command python).Path
Write-Host "Using Python at: $pythonPath" -ForegroundColor Yellow

# Run the initialization script
& $pythonPath verify_and_run.py

Write-Host "Press any key to continue..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 

# Install requirements
Write-Host "Installing required packages..." -ForegroundColor Green
pip install -r requirements.txt 

# Run the new interface
Write-Host "Running the new interface..." -ForegroundColor Green
python sovereign_interface.py 