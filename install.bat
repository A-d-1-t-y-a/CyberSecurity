@echo off
echo ========================================
echo   UNIFIED MEMORY FORENSICS FRAMEWORK
echo   INSTALLATION SCRIPT FOR WINDOWS
echo ========================================
echo.

echo [1/5] Creating virtual environment...
py -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo [2/5] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

echo [3/5] Upgrading pip...
py -m pip install --upgrade pip
if errorlevel 1 (
    echo ERROR: Failed to upgrade pip
    pause
    exit /b 1
)

echo [4/5] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [5/5] Installing framework...
pip install -e .
if errorlevel 1 (
    echo ERROR: Failed to install framework
    pause
    exit /b 1
)

echo.
echo ========================================
echo   INSTALLATION COMPLETED SUCCESSFULLY!
echo ========================================
echo.
echo To use the framework:
echo   1. Activate environment: venv\Scripts\activate
echo   2. Run framework: py -m unified_forensics --help
echo.
echo To test the framework:
echo   py -m unified_forensics info
echo.
pause
