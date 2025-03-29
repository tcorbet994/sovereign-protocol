# GitHub Setup Script for Sovereign Control Protocol

# Function to check if Git is installed
function Test-GitInstalled {
    try {
        git --version | Out-Null
        return $true
    } catch {
        return $false
    }
}

# Function to check if repository is already initialized
function Test-GitInitialized {
    return Test-Path .git
}

# Function to create necessary directories
function Initialize-Directories {
    Write-Host "Creating necessary directories..." -ForegroundColor Green
    $directories = @(
        "config",
        "security/biometric",
        "security/biometric/cache",
        "security/quantum",
        "security/quantum/state",
        "logs",
        "static"
    )
    
    foreach ($dir in $directories) {
        if (-not (Test-Path $dir)) {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
            Write-Host "Created directory: $dir" -ForegroundColor Yellow
        }
    }
}

# Main script
Write-Host "=== Sovereign Control Protocol GitHub Setup ===" -ForegroundColor Cyan

# Check Git installation
if (-not (Test-GitInstalled)) {
    Write-Host "Git is not installed. Please install Git first." -ForegroundColor Red
    exit 1
}

# Initialize directories
Initialize-Directories

# Initialize Git repository if not already initialized
if (-not (Test-GitInitialized)) {
    Write-Host "Initializing Git repository..." -ForegroundColor Green
    git init
    Write-Host "Git repository initialized." -ForegroundColor Yellow
}

# Add files to Git
Write-Host "Adding files to Git..." -ForegroundColor Green
git add .

# Initial commit
Write-Host "Creating initial commit..." -ForegroundColor Green
git commit -m "Initial commit: Sovereign Control Protocol"

# Get GitHub repository URL
$repoUrl = Read-Host "Enter your GitHub repository URL (e.g., https://github.com/username/sovereign-protocol.git)"

# Add remote repository
Write-Host "Adding remote repository..." -ForegroundColor Green
git remote add origin $repoUrl

# Push to GitHub
Write-Host "Pushing to GitHub..." -ForegroundColor Green
git push -u origin main

Write-Host "`nGitHub setup completed successfully!" -ForegroundColor Green
Write-Host "You can now access your repository at: $repoUrl" -ForegroundColor Yellow

# Display next steps
Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "1. Verify your repository on GitHub" -ForegroundColor White
Write-Host "2. Set up branch protection rules" -ForegroundColor White
Write-Host "3. Configure GitHub Actions if needed" -ForegroundColor White
Write-Host "4. Add collaborators if required" -ForegroundColor White

Write-Host "`nPress any key to continue..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 