@echo off
setlocal
echo ==============================================
echo Register mcp-gen globally (user PATH)
echo ==============================================

REM Resolve project root (this script is in /scripts)
set "SCRIPTS_DIR=%~dp0"
for %%I in ("%SCRIPTS_DIR%..") do set "PROJECT_ROOT=%%~fI"

echo Project root: %PROJECT_ROOT%

REM Check if already in PATH
echo %PATH% | find /I "%PROJECT_ROOT%" >nul
if %errorlevel%==0 (
  echo Already in PATH. Nothing to do.
  goto :end
)

echo Adding to user PATH ...
setx PATH "%PATH%;%PROJECT_ROOT%"
if %errorlevel% neq 0 (
  echo ERROR: Failed to update PATH.
  exit /b 1
)

echo Success. Please open a NEW terminal window to use 'mcp-gen' globally.

:end
endlocal
