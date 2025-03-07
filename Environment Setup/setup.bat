@echo off
setlocal

:: Check if Docker is installed
echo [INFO] Checking for Docker installation...
docker --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Docker is not installed.
    echo [INFO] Please install Docker and ensure it is running.
    exit /b
) ELSE (
    echo [INFO] Docker is installed.
)

:: Check if Docker Compose is installed
echo [INFO] Checking for Docker Compose installation...
docker-compose --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Docker Compose is not installed.
    echo [INFO] Please install Docker Compose.
    exit /b
) ELSE (
    echo [INFO] Docker Compose is installed.
)

:: Check if Firefox is installed
echo [INFO] Checking for Firefox installation...
reg query "HKLM\Software\Mozilla\Mozilla Firefox" >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [INFO] Firefox is not installed. Installing Firefox...
    :: Download Firefox installer
    powershell -Command "& {Invoke-WebRequest -Uri 'https://download.mozilla.org/?product=firefox-latest&os=win64&lang=en-US' -OutFile 'firefox_installer.exe'}"
    :: Install Firefox silently
    start /wait firefox_installer.exe -ms
    :: Clean up installer
    del firefox_installer.exe
    echo [INFO] Firefox installation completed.
) ELSE (
    echo [INFO] Firefox is installed.
)

:: Start Docker Compose to bring up the services
echo [INFO] Starting Docker containers using Docker Compose...
docker-compose -f docker-compose.yaml up -d

:: Wait for Elasticsearch containers to be fully initialized (check health status)
echo [INFO] Waiting for Elasticsearch containers to initialize...

:wait_for_elasticsearch
docker ps --filter "name=es" | findstr "Up" >nul
IF %ERRORLEVEL% NEQ 0 (
    echo [INFO] Elasticsearch containers are still initializing...
    timeout /t 10
    goto wait_for_elasticsearch
) ELSE (
    echo [INFO] Elasticsearch containers are running and healthy.
)

:: Check for Python version
echo [INFO] Checking for Python version between 3.12.0 and 3.13.0...

:: Get the full Python version (example: Python 3.12.3)
for /f "delims=" %%I in ('python --version 2^>^&1') do set PYTHON_VERSION=%%I

:: Extract major, minor, and patch version numbers using string manipulation
for /f "tokens=2 delims= " %%a in ("%PYTHON_VERSION%") do set PYTHON_VERSION_NUM=%%a
for /f "tokens=1-3 delims=." %%a in ("%PYTHON_VERSION_NUM%") do (
    set major=%%a
    set minor=%%b
    set patch=%%c
)

:: Check if Python version is within the allowed range (3.12.x to less than 3.13)
if %major% NEQ 3 (
    echo [ERROR] Python version is not 3.x. Please install a valid version of Python 3.
    exit /b
)

if %minor% LSS 12 (
    echo [ERROR] Python version is lower than 3.12.0. Installing Python 3.12.0...
    call :InstallPython312
    exit /b
)

if %minor% GEQ 13 (
    echo [ERROR] Python version is higher than 3.13.0. Please install Python 3.12.x or lower.
    exit /b
)

:: Python version is within the desired range (3.12.x and less than 3.13)
echo [INFO] Python version is %PYTHON_VERSION%.

:: Set up the virtual environment
echo [INFO] Setting up virtual environment...
python -m venv venv

:: Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate

:: Install dependencies from requirements.txt
echo [INFO] Installing dependencies from requirements.txt...
pip install --upgrade pip
pip install -r requirements.txt

echo [INFO] Environment setup completed successfully.

:: Pause to review
pause

exit /b

:: Function to download and install Python 3.12.0
:InstallPython312
echo [INFO] Downloading Python 3.12.0 installer...
powershell -Command "& {Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe' -OutFile 'python-3.12.0-amd64.exe'}"
echo [INFO] Installing Python 3.12.0...
start /wait python-3.12.0-amd64.exe /quiet InstallAllUsers=1 PrependPath=1
echo [INFO] Python 3.12.0 installation completed.