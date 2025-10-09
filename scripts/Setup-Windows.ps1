# Memory Forensics Framework - Windows PowerShell Setup
# Creates virtual environment and runs all 3 weeks

Write-Host "🚀 Memory Forensics Framework - Windows Setup" -ForegroundColor Green
Write-Host "=" * 50 -ForegroundColor Green

# Check Python installation
Write-Host "🔍 Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ $pythonVersion detected" -ForegroundColor Green
} catch {
    Write-Host "❌ Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from https://python.org" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if we're in the right directory
$projectRoot = Split-Path -Parent $PSScriptRoot
if (-not (Test-Path "$projectRoot/src")) {
    Write-Host "❌ Error: Please run this script from the project root directory" -ForegroundColor Red
    Write-Host "Expected structure: memory-forensics-framework/scripts/Setup-Windows.ps1" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "📁 Project root: $projectRoot" -ForegroundColor Cyan

# Run the Python setup script
Write-Host "`n🔧 Running Python setup script..." -ForegroundColor Yellow
try {
    Set-Location $projectRoot
    python scripts/windows_venv_setup.py
    
    Write-Host "`n🎉 Setup completed successfully!" -ForegroundColor Green
    Write-Host "`n📋 What was created:" -ForegroundColor Cyan
    Write-Host "- Virtual environment: venv/" -ForegroundColor White
    Write-Host "- Week 1 deliverables: week1/" -ForegroundColor White
    Write-Host "- Week 2 deliverables: week2/" -ForegroundColor White
    Write-Host "- Week 3 deliverables: week3/" -ForegroundColor White
    Write-Host "- Activation script: activate_venv.bat" -ForegroundColor White
    Write-Host "- Summary report: VENV_SETUP_SUMMARY.md" -ForegroundColor White
    
    Write-Host "`n🚀 Next steps:" -ForegroundColor Cyan
    Write-Host "1. Activate virtual environment: .\activate_venv.bat" -ForegroundColor White
    Write-Host "2. Run remaining weeks: python scripts/week4/setup.py" -ForegroundColor White
    Write-Host "3. Test framework: python -m pytest src/tests/ -v" -ForegroundColor White
    
} catch {
    Write-Host "❌ Setup failed: $_" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "`n✅ Windows setup completed successfully!" -ForegroundColor Green
Read-Host "Press Enter to exit"
