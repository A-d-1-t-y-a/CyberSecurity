@echo off
echo ========================================
echo   UNIFIED MEMORY FORENSICS FRAMEWORK
echo   SIMPLE SETUP SCRIPT
echo ========================================
echo.

echo [1/4] Creating virtual environment...
py -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    exit /b 1
)

echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    exit /b 1
)

echo [3/4] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    exit /b 1
)

echo [4/4] Installing framework...
pip install -e .
if errorlevel 1 (
    echo ERROR: Failed to install framework
    exit /b 1
)

echo.
echo ========================================
echo   SETUP COMPLETED SUCCESSFULLY!
echo ========================================
echo.
echo Framework is ready to use!
echo.
echo Quick test:
echo   py -m unified_forensics info
echo.
