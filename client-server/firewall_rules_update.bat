@echo off

:: chatgpt-code

echo Checking and configuring Windows Firewall Rules for Chat Server...
setlocal enabledelayedexpansion

:: Set port number (Change if needed)
set PORT=9090
set RULE_NAME_IN="Chat Server Inbound"
set RULE_NAME_OUT="Chat Server Outbound"

:: Check if the port is already in use
netstat -ano | findstr :%PORT% >nul
if %errorlevel% equ 0 (
    echo ERROR: Port %PORT% is already in use by another application.
    echo Please close the application using the port or choose a different one.
    pause
    exit /b
)

:: Check if inbound rule already exists
netsh advfirewall firewall show rule name=%RULE_NAME_IN% >nul 2>&1
if %errorlevel% equ 0 (
    echo Inbound rule already exists. Skipping...
) else (
    echo Adding inbound firewall rule for port %PORT%...
    netsh advfirewall firewall add rule name=%RULE_NAME_IN% dir=in action=allow protocol=TCP localport=%PORT%
)

:: Check if outbound rule already exists
netsh advfirewall firewall show rule name=%RULE_NAME_OUT% >nul 2>&1
if %errorlevel% equ 0 (
    echo Outbound rule already exists. Skipping...
) else (
    echo Adding outbound firewall rule for port %PORT%...
    netsh advfirewall firewall add rule name=%RULE_NAME_OUT% dir=out action=allow protocol=TCP localport=%PORT%
)

:: Enable ICMPv6 Echo Request for IPv6 pings
echo Enabling ICMPv6 Echo Request...
netsh advfirewall firewall set rule name="File and Printer Sharing (Echo Request - ICMPv6-In)" new enable=Yes

echo Firewall rules have been configured successfully!
pause
