# RALPH Build Script
Write-Host "Building RALPH Executable..." -ForegroundColor Green

# Ensure Python environment is active
if (Test-Path ".venv") {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    .\.venv\Scripts\Activate.ps1
} else {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
}

# Install required packages
Write-Host "Installing requirements..." -ForegroundColor Yellow
pip install -r requirements.txt
pip install pyinstaller

# Create spec file if it doesn't exist
$specContent = @"
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['sovereign_llm.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config', 'config'),
        ('static', 'static'),
        ('models', 'models'),
        ('security', 'security')
    ],
    hiddenimports=[
        'torch',
        'transformers',
        'fastapi',
        'uvicorn',
        'uvicorn.logging',
        'uvicorn.protocols',
        'websockets'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='RALPH',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='static/icon.ico'
)
"@

Set-Content -Path "ralph.spec" -Value $specContent

# Build the executable
Write-Host "Building executable..." -ForegroundColor Yellow
pyinstaller --clean ralph.spec

# Create launcher script
$launcherContent = @"
@echo off
echo Starting RALPH...
start "" "dist\RALPH.exe"
"@

Set-Content -Path "launch_ralph.bat" -Value $launcherContent

Write-Host "Build complete!" -ForegroundColor Green
Write-Host "You can find RALPH.exe in the dist folder" -ForegroundColor Green
Write-Host "Use launch_ralph.bat to start RALPH" -ForegroundColor Green

# Deactivate virtual environment
deactivate 