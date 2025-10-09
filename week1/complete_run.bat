@echo off
REM Week 1 Complete Run Script - Windows
REM Cross-Platform Unified Memory Forensics Framework
REM Student: Manoj Santhoju (ID: 23394544)
REM Institution: National College of Ireland

setlocal enabledelayedexpansion

REM Configuration
set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..
set LOG_FILE=%SCRIPT_DIR%logs\validation.log

REM Create logs directory if it doesn't exist
if not exist "%SCRIPT_DIR%logs" mkdir "%SCRIPT_DIR%logs"

REM Colors for output (Windows 10+)
set "RED=[91m"
set "GREEN=[92m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "NC=[0m"

echo %BLUE%[%date% %time%]%NC% Starting Week 1 Complete Run Script

REM Step 1: Setup
echo %BLUE%[%date% %time%]%NC% Running Week 1 Setup...
python "%SCRIPT_DIR%setup.py"
if %errorlevel% neq 0 (
    echo %RED%[ERROR]%NC% Week 1 setup failed
    goto :error
)
echo %GREEN%[SUCCESS]%NC% Week 1 setup completed

REM Step 2: Analysis
echo %BLUE%[%date% %time%]%NC% Running Week 1 Analysis...
python "%SCRIPT_DIR%analysis.py"
if %errorlevel% neq 0 (
    echo %RED%[ERROR]%NC% Week 1 analysis failed
    goto :error
)
echo %GREEN%[SUCCESS]%NC% Week 1 analysis completed

REM Step 3: Reports
echo %BLUE%[%date% %time%]%NC% Running Week 1 Reports...
python "%SCRIPT_DIR%reports.py"
if %errorlevel% neq 0 (
    echo %RED%[ERROR]%NC% Week 1 reports failed
    goto :error
)
echo %GREEN%[SUCCESS]%NC% Week 1 reports completed

REM Step 4: Presentation
echo %BLUE%[%date% %time%]%NC% Running Week 1 Presentation...
python "%SCRIPT_DIR%presentation.py"
if %errorlevel% neq 0 (
    echo %RED%[ERROR]%NC% Week 1 presentation failed
    goto :error
)
echo %GREEN%[SUCCESS]%NC% Week 1 presentation completed

REM Step 5: Validation
echo %BLUE%[%date% %time%]%NC% Validating Week 1 deliverables...

REM Check required files
set "MISSING_FILES="
if not exist "%SCRIPT_DIR%setup.py" set "MISSING_FILES=%MISSING_FILES% setup.py"
if not exist "%SCRIPT_DIR%analysis.py" set "MISSING_FILES=%MISSING_FILES% analysis.py"
if not exist "%SCRIPT_DIR%reports.py" set "MISSING_FILES=%MISSING_FILES% reports.py"
if not exist "%SCRIPT_DIR%presentation.py" set "MISSING_FILES=%MISSING_FILES% presentation.py"
if not exist "%SCRIPT_DIR%complete_run.py" set "MISSING_FILES=%MISSING_FILES% complete_run.py"
if not exist "%SCRIPT_DIR%explanations.txt" set "MISSING_FILES=%MISSING_FILES% explanations.txt"
if not exist "%SCRIPT_DIR%report.md" set "MISSING_FILES=%MISSING_FILES% report.md"
if not exist "%SCRIPT_DIR%reports\literature_review.md" set "MISSING_FILES=%MISSING_FILES% reports\literature_review.md"
if not exist "%SCRIPT_DIR%reports\tool_analysis.md" set "MISSING_FILES=%MISSING_FILES% reports\tool_analysis.md"
if not exist "%SCRIPT_DIR%presentations\presentation.md" set "MISSING_FILES=%MISSING_FILES% presentations\presentation.md"

if not "%MISSING_FILES%"=="" (
    echo %YELLOW%[WARNING]%NC% Missing files:%MISSING_FILES%
    goto :warning
)

echo %GREEN%[SUCCESS]%NC% All Week 1 deliverables validated

REM Step 6: Line count check
echo %BLUE%[%date% %time%]%NC% Checking line counts...

for %%f in (setup.py analysis.py reports.py presentation.py complete_run.py) do (
    for /f %%i in ('find /c /v "" ^< "%SCRIPT_DIR%%%f"') do (
        if %%i gtr 300 (
            echo %YELLOW%[WARNING]%NC% %%f has %%i lines (exceeds 300 limit)
        ) else (
            echo %GREEN%[INFO]%NC% %%f has %%i lines (within limit)
        )
    )
)

REM Step 7: Git operations
echo %BLUE%[%date% %time%]%NC% Running git operations...

cd /d "%PROJECT_ROOT%"

REM Add Week 1 files
git add week1/
if %errorlevel% neq 0 (
    echo %YELLOW%[WARNING]%NC% Git add failed
    goto :warning
)

REM Commit changes
for /f "tokens=1-3 delims=/ " %%a in ('date /t') do set "DATE=%%c-%%a-%%b"
for /f "tokens=1-2 delims=: " %%a in ('time /t') do set "TIME=%%a:%%b"
set "COMMIT_MSG=Week 1: Foundation ^& Literature Review - Complete deliverables generated (%DATE% %TIME%)"

git commit -m "%COMMIT_MSG%"
if %errorlevel% neq 0 (
    echo %YELLOW%[WARNING]%NC% Git commit failed
    goto :warning
)

REM Push to remote
git push origin main
if %errorlevel% neq 0 (
    echo %YELLOW%[WARNING]%NC% Git push failed
    goto :warning
)

echo %GREEN%[SUCCESS]%NC% Git operations completed

REM Success
echo.
echo ============================================================
echo Week 1 Complete Run - SUCCESS
echo ============================================================
echo All Week 1 deliverables have been generated successfully.
echo Check the week1\ directory for all outputs.
echo ============================================================
exit /b 0

:warning
echo.
echo ============================================================
echo Week 1 Complete Run - WARNING
echo ============================================================
echo Some Week 1 deliverables may have issues.
echo Check the logs in week1\logs\ for details.
echo ============================================================
exit /b 1

:error
echo.
echo ============================================================
echo Week 1 Complete Run - FAILED
echo ============================================================
echo Some Week 1 deliverables failed to generate.
echo Check the logs in week1\logs\ for details.
echo ============================================================
exit /b 1
