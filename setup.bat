@echo off
title PhantomTrack - Setup
color 0C

echo.
echo  =========================================
echo   PHANTOMTRACK - SETUP
echo  =========================================
echo.

echo [*] Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [!] pip failed. Make sure Python is installed and in PATH.
    echo     Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo.
echo [*] Checking for cloudflared.exe...
IF NOT EXIST "cloudflared.exe" (
    echo [*] Downloading cloudflared.exe...
    powershell -Command "Invoke-WebRequest -Uri 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe' -OutFile 'cloudflared.exe'"
    if %errorlevel% neq 0 (
        echo [!] Download failed. Check your internet connection.
        pause
        exit /b 1
    )
    echo [+] cloudflared.exe ready.
) ELSE (
    echo [+] cloudflared.exe already present.
)

echo.
echo  =========================================
echo   [+] Setup complete. Run: .\run.bat
echo  =========================================
echo.
pause
