# PowerShell Setup Script for Memory Forensics Framework
# Windows-specific setup and configuration

param(
    [switch]$Force,
    [switch]$SkipTests,
    [string]$PythonPath = "python"
)

Write-Host "🚀 Memory Forensics Framework Setup (Windows)" -ForegroundColor Green
Write-Host "=" * 50

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")

if (-not $isAdmin) {
    Write-Warning "⚠️  Running without administrator privileges. Some features may not work correctly."
}

# Function to run command and return result
function Invoke-CommandWithResult {
    param(
        [string]$Command,
        [string]$WorkingDirectory = $PWD
    )
    
    try {
        $result = Invoke-Expression $Command
        return @{
            Success = $true
            Output = $result
            Error = $null
        }
    }
    catch {
        return @{
            Success = $false
            Output = $null
            Error = $_.Exception.Message
        }
    }
}

# Check Python installation
Write-Host "🐍 Checking Python installation..." -ForegroundColor Yellow
$pythonVersion = & $PythonPath --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "❌ Python not found. Please install Python 3.9+" -ForegroundColor Red
    Write-Host "Download from: https://www.python.org/downloads/" -ForegroundColor Cyan
    exit 1
}

# Check pip installation
Write-Host "📦 Checking pip installation..." -ForegroundColor Yellow
$pipVersion = & $PythonPath -m pip --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ pip found: $pipVersion" -ForegroundColor Green
} else {
    Write-Host "❌ pip not found. Please install pip" -ForegroundColor Red
    exit 1
}

# Install Python requirements
Write-Host "📦 Installing Python requirements..." -ForegroundColor Yellow
$installResult = Invoke-CommandWithResult "$PythonPath -m pip install -r requirements.txt"
if ($installResult.Success) {
    Write-Host "✅ Python requirements installed successfully" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to install requirements: $($installResult.Error)" -ForegroundColor Red
    exit 1
}

# Install memory forensics tools
Write-Host "🔧 Installing memory forensics tools..." -ForegroundColor Yellow
$tools = @("volatility3", "rekall", "psutil", "yara-python")

foreach ($tool in $tools) {
    Write-Host "Installing $tool..." -ForegroundColor Cyan
    $toolResult = Invoke-CommandWithResult "$PythonPath -m pip install $tool"
    if ($toolResult.Success) {
        Write-Host "✅ $tool installed successfully" -ForegroundColor Green
    } else {
        Write-Host "❌ Failed to install $tool : $($toolResult.Error)" -ForegroundColor Red
    }
}

# Create project directories
Write-Host "📁 Creating project directories..." -ForegroundColor Yellow
$directories = @(
    "src\framework",
    "src\utils", 
    "src\tests",
    "docs\reports",
    "docs\guides",
    "docs\presentations",
    "data\dumps",
    "data\results",
    "logs",
    "week1", "week2", "week3", "week4", "week5", "week6", "week7"
)

foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "✅ Created directory: $dir" -ForegroundColor Green
    } else {
        Write-Host "ℹ️  Directory already exists: $dir" -ForegroundColor Blue
    }
}

# Create .gitignore
Write-Host "📝 Creating .gitignore..." -ForegroundColor Yellow
$gitignoreContent = @"
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Memory dumps and sensitive data
data/dumps/*.dmp
data/dumps/*.raw
data/dumps/*.vmem
data/results/*.json
*.log

# OS specific
.DS_Store
Thumbs.db

# Project specific
logs/
temp/
cache/
"@

Set-Content -Path ".gitignore" -Value $gitignoreContent
Write-Host "✅ .gitignore created" -ForegroundColor Green

# Setup Git repository
Write-Host "🔧 Setting up Git repository..." -ForegroundColor Yellow
if (-not (Test-Path ".git")) {
    $gitInitResult = Invoke-CommandWithResult "git init"
    if ($gitInitResult.Success) {
        Write-Host "✅ Git repository initialized" -ForegroundColor Green
        
        # Add all files
        Invoke-CommandWithResult "git add ." | Out-Null
        
        # Make initial commit
        Invoke-CommandWithResult 'git commit -m "Initial commit: Framework setup"'
        Write-Host "✅ Initial commit created" -ForegroundColor Green
    } else {
        Write-Host "❌ Failed to initialize git: $($gitInitResult.Error)" -ForegroundColor Red
    }
} else {
    Write-Host "✅ Git repository already initialized" -ForegroundColor Green
}

# Verify installation
Write-Host "🔍 Verifying installation..." -ForegroundColor Yellow
$testImports = @("volatility3", "rekall", "psutil", "yara")

foreach ($module in $testImports) {
    $importResult = Invoke-CommandWithResult "$PythonPath -c `"import $module; print('$module import successful')`""
    if ($importResult.Success) {
        Write-Host "✅ $module import successful" -ForegroundColor Green
    } else {
        Write-Host "❌ $module import failed: $($importResult.Error)" -ForegroundColor Red
    }
}

# Run tests if not skipped
if (-not $SkipTests) {
    Write-Host "🧪 Running basic tests..." -ForegroundColor Yellow
    $testResult = Invoke-CommandWithResult "$PythonPath -m pytest src/tests/ -v"
    if ($testResult.Success) {
        Write-Host "✅ Tests passed successfully" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Some tests failed: $($testResult.Error)" -ForegroundColor Yellow
    }
}

Write-Host "=" * 50
Write-Host "🎉 Windows setup completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Run tests: pytest src/tests/ -v" -ForegroundColor White
Write-Host "2. Start with Week 1: python scripts/week1/setup.py" -ForegroundColor White
Write-Host "3. Read documentation: docs/guides/user_guide.md" -ForegroundColor White
Write-Host ""
Write-Host "For PowerShell-specific features, run:" -ForegroundColor Cyan
Write-Host "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor White
