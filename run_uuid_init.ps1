Write-Host "Setting up Sovereign Control Protocol..." -ForegroundColor Green

# Run the initialization script
python simple_uuid_init.py

Write-Host "Press any key to continue..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 