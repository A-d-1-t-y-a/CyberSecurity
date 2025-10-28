@echo off
REM Unified Memory Forensics Framework - Windows Test Script
REM Author: Manoj Santhoju
REM Institution: National College of Ireland

echo ================================================================================
echo UNIFIED MEMORY FORENSICS FRAMEWORK - WINDOWS TESTING
echo ================================================================================

REM Activate virtual environment
call venv\Scripts\activate.bat

echo.
echo [1] Testing Framework Info...
py -m unified_forensics info
if %errorlevel% neq 0 (
    echo ERROR: Framework info test failed
    goto :error
)
echo SUCCESS: Framework info test passed

echo.
echo [2] Testing Memory Sample Generation...
py quick_sample_generator.py
if %errorlevel% neq 0 (
    echo ERROR: Memory sample generation failed
    goto :error
)
echo SUCCESS: Memory sample generation test passed

echo.
echo [3] Testing Windows Analysis...
py -m unified_forensics analyze memory_dump_samples/windows_sample.mem --os-type windows --format summary
if %errorlevel% neq 0 (
    echo ERROR: Windows analysis test failed
    goto :error
)
echo SUCCESS: Windows analysis test passed

echo.
echo [4] Testing Linux Analysis...
py -m unified_forensics analyze memory_dump_samples/linux_sample.mem --os-type linux --format summary
if %errorlevel% neq 0 (
    echo ERROR: Linux analysis test failed
    goto :error
)
echo SUCCESS: Linux analysis test passed

echo.
echo [5] Testing macOS Analysis...
py -m unified_forensics analyze memory_dump_samples/macos_sample.mem --os-type macos --format summary
if %errorlevel% neq 0 (
    echo ERROR: macOS analysis test failed
    goto :error
)
echo SUCCESS: macOS analysis test passed

echo.
echo [6] Testing Experimental Analysis...
py -m unified_forensics experiment memory_dump_samples/windows_sample.mem --os-type windows --rates 1 --rates 10 --output analysis_results/windows_experimental_test.json
if %errorlevel% neq 0 (
    echo ERROR: Experimental analysis test failed
    goto :error
)
echo SUCCESS: Experimental analysis test passed

echo.
echo [7] Testing Cross-Platform Validation...
py -m unified_forensics validate --windows-dump memory_dump_samples/windows_sample.mem --linux-dump memory_dump_samples/linux_sample.mem --macos-dump memory_dump_samples/macos_sample.mem --output analysis_results/cross_platform_validation_test.json
if %errorlevel% neq 0 (
    echo ERROR: Cross-platform validation test failed
    goto :error
)
echo SUCCESS: Cross-platform validation test passed

echo.
echo ================================================================================
echo ALL TESTS PASSED SUCCESSFULLY!
echo ================================================================================
echo.
echo Framework is ready for Professor Presentation on Windows!
echo.
echo Generated Files:
echo   - Memory Samples: memory_dump_samples/
echo   - Analysis Results: analysis_results/
echo   - Performance Charts: performance_charts/
echo.
echo ================================================================================
goto :end

:error
echo.
echo ================================================================================
echo TEST FAILED!
echo ================================================================================
echo Please check the error messages above and fix any issues.
echo ================================================================================
exit /b 1

:end
pause
