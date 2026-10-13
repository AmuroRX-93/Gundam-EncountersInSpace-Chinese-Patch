@echo off
setlocal
chcp 65001 >nul
set "ARCH=%PROCESSOR_ARCHITECTURE%"
if defined PROCESSOR_ARCHITEW6432 set "ARCH=%PROCESSOR_ARCHITEW6432%"
set "RUNTIME="
if /I "%ARCH%"=="AMD64" set "RUNTIME=windows-x64"
if /I "%ARCH%"=="ARM64" set "RUNTIME=windows-arm64"
if not defined RUNTIME (
 echo Unsupported Windows architecture: %ARCH%
 pause
 exit /b 1
)
set "PYTHON=%~dp0runtime\%RUNTIME%\python.exe"
if not exist "%PYTHON%" (
 echo ERROR: Bundled Python is missing. Extract the COMPLETE Encounter in Space ALLPLATFORM 1.0.1 package.
 echo This tool cannot run from inside the ZIP file.
 pause
 exit /b 1
)
"%PYTHON%" -I -B -X utf8 "%~dp0launch.py" %*
set "RESULT=%ERRORLEVEL%"
if not "%RESULT%"=="0" echo ERROR: Operation failed. Read the error above and the included instructions.
pause
exit /b %RESULT%
