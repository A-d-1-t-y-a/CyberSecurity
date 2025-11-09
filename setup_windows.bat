@echo off
REM Unified Memory Forensics Framework - Windows Setup Script
REM Author: Manoj Santhoju
REM Institution: National College of Ireland
REM Program: MSc Cybersecurity

echo ================================================================================
echo UNIFIED MEMORY FORENSICS FRAMEWORK - WINDOWS SETUP
echo ================================================================================
echo Author: Manoj Santhoju
echo Institution: National College of Ireland
echo Program: MSc Cybersecurity
echo ================================================================================

echo.
echo [1] Checking Python installation...
py --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11+ from https://python.org
    pause
    exit /b 1
)
echo SUCCESS: Python is installed

echo.
echo [2] Creating virtual environment...
if exist venv (
    echo SUCCESS: Virtual environment already exists
) else (
    py -m venv venv
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo SUCCESS: Virtual environment created
)

echo.
echo [3] Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo SUCCESS: Virtual environment activated

echo.
echo [4] Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo SUCCESS: Dependencies installed

echo.
echo [5] Installing framework...
pip install -e .
if %errorlevel% neq 0 (
    echo ERROR: Failed to install framework
    pause
    exit /b 1
)
echo SUCCESS: Framework installed

echo.
echo [6] Creating directories...
if not exist memory_dump_samples mkdir memory_dump_samples
if not exist analysis_results mkdir analysis_results
if not exist performance_charts mkdir performance_charts
if not exist logs mkdir logs
echo SUCCESS: Directories created

echo.
echo [7] Testing framework...
py -m unified_forensics info
if %errorlevel% neq 0 (
    echo ERROR: Framework test failed
    pause
    exit /b 1
)
echo SUCCESS: Framework test passed

echo.
echo ================================================================================
echo SETUP COMPLETED SUCCESSFULLY!
echo ================================================================================
echo.
echo To run malware testing:
echo   test_complete_malware.bat
echo.
echo To run individual commands:
echo   py -m unified_forensics analyze memory_dump.mem
echo   py -m unified_forensics experiment memory_dump.mem --os-type windows
echo.
echo Ready for Professor Presentation!
echo ================================================================================
pause
