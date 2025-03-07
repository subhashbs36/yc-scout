:: Activate the Python virtual environment
echo Activating Python virtual environment...
call venv\Scripts\activate
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to activate virtual environment.
    exit /b 1
)

@echo off
python SearchQuery.py
pause
