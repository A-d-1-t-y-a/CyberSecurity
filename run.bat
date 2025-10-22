@echo off
echo ========================================
echo   UNIFIED MEMORY FORENSICS FRAMEWORK
echo   QUICK START SCRIPT
echo ========================================
echo.

echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Virtual environment not found. Please run install.bat first.
    pause
    exit /b 1
)

echo.
echo Framework is ready! Available commands:
echo.
echo   py -m unified_forensics --help          - Show help
echo   py -m unified_forensics info             - Show framework info
echo   py -m unified_forensics analyze dump.mem - Analyze memory dump
echo.
echo Example usage:
echo   py -m unified_forensics analyze memory_dump.mem --os windows
echo.

py -m unified_forensics --help
