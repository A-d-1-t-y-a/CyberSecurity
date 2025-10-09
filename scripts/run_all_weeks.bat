@echo off
echo ========================================
echo Memory Forensics Framework - Windows Setup
echo ========================================
echo.

echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo.
echo Creating virtual environment and running all 3 weeks...
echo.

python scripts/windows_venv_setup.py

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To activate the virtual environment:
echo   activate_venv.bat
echo.
echo To run additional weeks:
echo   python scripts/week4/setup.py
echo   python scripts/week5/setup.py
echo   python scripts/week6/setup.py
echo   python scripts/week7/setup.py
echo.
echo To run all weeks at once:
echo   python scripts/master_setup.py
echo.
pause
