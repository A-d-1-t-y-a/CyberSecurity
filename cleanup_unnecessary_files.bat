@echo off
REM Cleanup Unnecessary Files
REM Author: Manoj Santhoju

echo ==========================================
echo CLEANUP UNNECESSARY FILES
echo ==========================================
echo.

echo Removing duplicate/redundant documentation files...
del /q CROSS_PLATFORM_GUIDE.md 2>nul
del /q FINAL_CROSS_PLATFORM_SUMMARY.md 2>nul
del /q FINAL_PROJECT_SUMMARY.md 2>nul
del /q GRAPH_FIX_GUIDE.md 2>nul
del /q MALWARE_TESTING_GUIDE.md 2>nul
del /q MALWARE_TESTING_SUMMARY.md 2>nul
del /q QUICK_FIX_INSTRUCTIONS.md 2>nul
del /q QUICK_MALWARE_TEST.md 2>nul

echo Removing duplicate test scripts...
del /q cleanup_malware_test.bat 2>nul
del /q cleanup_malware_test.sh 2>nul
del /q quick_fix_malware_test.bat 2>nul
del /q test_malware_detection.bat 2>nul
del /q test_malware_detection.sh 2>nul

echo Removing old analysis results...
if exist analysis_results (
    del /q analysis_results\*.json 2>nul
)

echo Removing test artifacts (will be recreated)...
if exist malware_test_environment (
    rmdir /s /q malware_test_environment
)
if exist memory_dump_with_malware.raw (
    del /q memory_dump_with_malware.raw
)

echo Removing old performance charts (will be recreated)...
if exist performance_charts (
    del /q performance_charts\*.png 2>nul
)

echo.
echo ==========================================
echo CLEANUP COMPLETE
echo ==========================================
echo.
echo Removed:
echo   - Duplicate documentation files
echo   - Redundant test scripts
echo   - Old analysis results
echo   - Test artifacts
echo.
echo Kept essential files:
echo   - Core framework
echo   - Main test scripts
echo   - Setup scripts
echo   - README.md
echo.
pause
