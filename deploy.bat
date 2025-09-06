@echo off
REM SME Debt Management Tool - Windows Deployment Script
REM This script deploys the application on Windows Server

echo Starting deployment of SME Debt Management Tool...

REM Configuration
set APP_NAME=sme-debt-tool
set APP_DIR=C:\inetpub\wwwroot\%APP_NAME%
set PYTHON_PATH=C:\Python311
set SERVICE_NAME=SME-Debt-Tool

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Running as administrator - OK
) else (
    echo ERROR: This script must be run as administrator
    pause
    exit /b 1
)

REM Check Python installation
echo Checking Python installation...
%PYTHON_PATH%\python.exe --version >nul 2>&1
if %errorLevel% == 0 (
    echo Python found - OK
) else (
    echo ERROR: Python not found at %PYTHON_PATH%
    echo Please install Python 3.11 or update the PYTHON_PATH variable
    pause
    exit /b 1
)

REM Create application directory
echo Creating application directory...
if not exist "%APP_DIR%" mkdir "%APP_DIR%"
if not exist "%APP_DIR%\logs" mkdir "%APP_DIR%\logs"

REM Copy application files
echo Copying application files...
xcopy /E /I /Y . "%APP_DIR%"

REM Install Python dependencies
echo Installing Python dependencies...
cd /d "%APP_DIR%"
%PYTHON_PATH%\python.exe -m pip install -r requirements.txt

REM Create Windows service using NSSM (Non-Sucking Service Manager)
echo Creating Windows service...
if exist "C:\nssm\nssm.exe" (
    C:\nssm\nssm.exe install "%SERVICE_NAME%" "%PYTHON_PATH%\python.exe" "%APP_DIR%\app.py"
    C:\nssm\nssm.exe set "%SERVICE_NAME%" AppDirectory "%APP_DIR%"
    C:\nssm\nssm.exe set "%SERVICE_NAME%" AppEnvironmentExtra "FLASK_ENV=production"
    C:\nssm\nssm.exe set "%SERVICE_NAME%" AppStdout "%APP_DIR%\logs\service.log"
    C:\nssm\nssm.exe set "%SERVICE_NAME%" AppStderr "%APP_DIR%\logs\service_error.log"
    C:\nssm\nssm.exe start "%SERVICE_NAME%"
    echo Service created and started
) else (
    echo WARNING: NSSM not found. Please install NSSM to create a Windows service.
    echo You can download it from: https://nssm.cc/download
    echo For now, you can run the application manually with: python app.py
)

REM Configure IIS (if available)
echo Configuring IIS...
if exist "C:\Windows\System32\inetsrv\inetmgr.exe" (
    echo IIS is available - you can configure it manually
    echo 1. Open IIS Manager
    echo 2. Create a new site pointing to %APP_DIR%
    echo 3. Configure URL rewrite rules for Flask
) else (
    echo IIS not found - skipping IIS configuration
)

REM Configure Windows Firewall
echo Configuring Windows Firewall...
netsh advfirewall firewall add rule name="SME Debt Tool HTTP" dir=in action=allow protocol=TCP localport=5000
netsh advfirewall firewall add rule name="SME Debt Tool HTTPS" dir=in action=allow protocol=TCP localport=443

REM Create startup script
echo Creating startup script...
echo @echo off > "%APP_DIR%\start.bat"
echo cd /d "%APP_DIR%" >> "%APP_DIR%\start.bat"
echo %PYTHON_PATH%\python.exe app.py >> "%APP_DIR%\start.bat"

REM Create stop script
echo Creating stop script...
echo @echo off > "%APP_DIR%\stop.bat"
echo taskkill /f /im python.exe >> "%APP_DIR%\stop.bat"

echo.
echo ========================================
echo Deployment completed successfully!
echo ========================================
echo.
echo Application directory: %APP_DIR%
echo Service name: %SERVICE_NAME%
echo.
echo To start the application manually:
echo   %APP_DIR%\start.bat
echo.
echo To stop the application:
echo   %APP_DIR%\stop.bat
echo.
echo To check service status:
echo   sc query "%SERVICE_NAME%"
echo.
echo The application should be available at:
echo   http://localhost:5000
echo.
echo Remember to:
echo 1. Configure your domain name
echo 2. Set up SSL certificates
echo 3. Configure monitoring
echo 4. Set up backups
echo.
pause
