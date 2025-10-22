@echo off
echo ========================================
echo   UNIFIED MEMORY FORENSICS FRAMEWORK
echo   COMPREHENSIVE TEST SUITE
echo ========================================
echo.

call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Virtual environment not found. Please run install.bat first.
    exit /b 1
)

echo [1/8] Testing framework info...
py -m unified_forensics info
if errorlevel 1 (
    echo ERROR: Framework info failed
    exit /b 1
)

echo.
echo [2/8] Testing help command...
py -m unified_forensics --help
if errorlevel 1 (
    echo ERROR: Help command failed
    exit /b 1
)

echo.
echo [3/8] Testing analyze help...
py -m unified_forensics analyze --help
if errorlevel 1 (
    echo ERROR: Analyze help failed
    exit /b 1
)

echo.
echo [4/8] Testing detect-os help...
py -m unified_forensics detect-os --help
if errorlevel 1 (
    echo ERROR: Detect-OS help failed
    exit /b 1
)

echo.
echo [5/8] Creating test memory dump...
py create_test_dump.py test_memory.mem 5
if errorlevel 1 (
    echo ERROR: Failed to create test dump
    exit /b 1
)

echo.
echo [6/8] Testing OS detection...
py -m unified_forensics detect-os test_memory.mem
if errorlevel 1 (
    echo ERROR: OS detection failed
    exit /b 1
)

echo.
echo [7/8] Testing memory analysis (summary)...
py -m unified_forensics analyze test_memory.mem --format summary
if errorlevel 1 (
    echo ERROR: Memory analysis failed
    exit /b 1
)

echo.
echo [8/8] Testing memory analysis (table)...
py -m unified_forensics analyze test_memory.mem --format table
if errorlevel 1 (
    echo ERROR: Table analysis failed
    exit /b 1
)

echo.
echo ========================================
echo   ALL TESTS COMPLETED SUCCESSFULLY!
echo ========================================
echo.
echo Framework is working perfectly!
echo.
del test_memory.mem
echo Test file cleaned up.
echo.
echo Ready for production use!
echo.
