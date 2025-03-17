@echo off

:: Check if Node.js is installed
node -v >nul 2>&1
if %errorlevel% neq 0 (
    echo Node.js is not installed. Installing Node.js...
    :: Download and install Node.js (this example uses the Windows installer)
    powershell -Command "Invoke-WebRequest -Uri https://nodejs.org/dist/v16.13.0/node-v16.13.0-x64.msi -OutFile nodejs.msi"
    msiexec /i nodejs.msi /quiet /norestart
    del nodejs.msi
) else (
    echo Node.js is already installed.
)

:: Run npm install
echo Running npm install...
npm install