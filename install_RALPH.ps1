# RALPH Installation and Build Script
$ErrorActionPreference = "Stop"

Write-Host "RALPH Installation and Build Process" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan

# Configuration
$config = @{
    ProjectName = "RALPH"
    VirtualEnv = ".venv"
    RequiredPython = "3.10"
    MainScript = "sovereign_llm.py"
    OutputName = "RALPH"
}

# Function definitions
function Test-PythonInstallation {
    try {
        $pythonVersion = python --version
        Write-Host "Found Python: $pythonVersion" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "Python not found. Please install Python $($config.RequiredPython) or higher." -ForegroundColor Red
        return $false
    }
}

function Initialize-VirtualEnvironment {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv $config.VirtualEnv
    
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & "$($config.VirtualEnv)\Scripts\Activate.ps1"
    
    Write-Host "Installing required packages..." -ForegroundColor Yellow
    pip install --upgrade pip
    pip install -r requirements.txt
    pip install pyinstaller
}

function New-RALPHExecutable {
    Write-Host "Building RALPH executable..." -ForegroundColor Yellow
    
    # Create PyInstaller spec
    $specContent = @"
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['$($config.MainScript)'],
    pathex=[],
    binaries=[],
    datas=[
        ('config', 'config'),
        ('static', 'static'),
        ('models', 'models'),
        ('security', 'security'),
        ('sovereign_control', 'sovereign_control')
    ],
    hiddenimports=[
        'torch',
        'transformers',
        'fastapi',
        'uvicorn',
        'uvicorn.logging',
        'uvicorn.protocols',
        'websockets',
        'numpy',
        'scipy'
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
    name='$($config.OutputName)',
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

    Set-Content -Path "RALPH.spec" -Value $specContent
    
    # Build executable
    pyinstaller --clean RALPH.spec
}

function New-LauncherScript {
    Write-Host "Creating launcher script..." -ForegroundColor Yellow
    
    $launcherContent = @"
@echo off
echo Starting RALPH...
echo Initializing consciousness interface...
start "" "dist\RALPH.exe"
"@

    Set-Content -Path "launch_RALPH.bat" -Value $launcherContent
}

function Initialize-RALPHStructure {
    Write-Host "Creating directory structure..." -ForegroundColor Yellow
    
    $directories = @(
        "config",
        "static",
        "models",
        "security",
        "sovereign_control"
    )
    
    foreach ($dir in $directories) {
        if (-not (Test-Path $dir)) {
            New-Item -ItemType Directory -Path $dir
        }
    }
}

# Main installation process
try {
    Write-Host "Beginning RALPH installation..." -ForegroundColor Green
    
    # Check Python installation
    if (-not (Test-PythonInstallation)) {
        exit 1
    }
    
    # Create project structure
    Initialize-RALPHStructure
    
    # Set up virtual environment
    Initialize-VirtualEnvironment
    
    # Build executable
    New-RALPHExecutable
    
    # Create launcher
    New-LauncherScript
    
    Write-Host "`nRALPH installation complete!" -ForegroundColor Green
    Write-Host "You can find RALPH.exe in the dist folder" -ForegroundColor Green
    Write-Host "Use launch_RALPH.bat to start RALPH" -ForegroundColor Green
}
catch {
    Write-Host "An error occurred during installation: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
finally {
    # Deactivate virtual environment if active
    if ($env:VIRTUAL_ENV) {
        deactivate
    }
}