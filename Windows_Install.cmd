@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"
if not exist "%~dp0runtime\windows-x64\python.exe" (
  echo Missing bundled Python. Extract the WHOLE ZIP first.
  pause
  exit /b 1
)
"%~dp0runtime\windows-x64\python.exe" -I "%~dp0install.py" %*
set "rc=%errorlevel%"
echo.
pause
exit /b %rc%
