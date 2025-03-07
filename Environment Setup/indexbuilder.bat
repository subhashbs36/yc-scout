@echo off
setlocal enabledelayedexpansion

:: Activate the Python virtual environment
echo Activating Python virtual environment...
call venv\Scripts\activate
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to activate virtual environment.
    exit /b 1
)

:: Set default input file
set SOURCE_FILE=output.jl

:: Check if an argument is provided (optional input file)
if not "%~1"=="" set SOURCE_FILE=%~1

:: Check if the "pyelastic" container is running
echo Checking if pyelastic container is running...
docker ps | findstr "yc-scraper" >nul

if %errorlevel% neq 0 (
    echo pyelastic is NOT running. Starting container...
    docker start pyelastic
    timeout /t 5 /nobreak >nul  :: Wait for 5 seconds to allow it to start
) else (
    echo pyelastic is already running.
)

:: Run the Python script with the specified input file
echo Running Python script with %SOURCE_FILE%...
python PyElasticDumper.py %SOURCE_FILE%

echo Script execution completed.
pause
