@echo off
REM Auto-commit script for Auto DevOps Assistant
REM This script will automatically stage, commit, and push all changes

echo 🚀 Auto DevOps Assistant - Automatic Commit Script
echo ====================================================
echo.

REM Check if we're in the right directory
if not exist "backend\app.py" (
    echo ❌ Error: Not in the correct directory
    echo Please run this script from the auto-devops-assistant root folder
    pause
    exit /b 1
)

REM Check git status
echo 📋 Checking git status...
git status --porcelain > temp_status.txt

REM Check if there are any changes
for /f %%i in ('find /c /v "" ^< temp_status.txt') do set line_count=%%i
del temp_status.txt

if %line_count%==0 (
    echo ✅ No changes detected - repository is clean
    echo.
    pause
    exit /b 0
)

echo 📝 Changes detected! Preparing automatic commit...
echo.

REM Generate timestamp for commit message
for /f "tokens=1-4 delims=/ " %%i in ('date /t') do set COMMIT_DATE=%%i-%%j-%%k
for /f "tokens=1-2 delims=: " %%i in ('time /t') do set COMMIT_TIME=%%i:%%j
set TIMESTAMP=%COMMIT_DATE% %COMMIT_TIME%

REM Stage all changes
echo 📦 Staging all changes...
git add .
if errorlevel 1 (
    echo ❌ Failed to stage changes
    pause
    exit /b 1
)

REM Create automatic commit message
set COMMIT_MSG=🔄 Auto-commit: Updates at %TIMESTAMP%

REM Allow user to customize commit message
echo.
echo Default commit message: "%COMMIT_MSG%"
echo.
set /p CUSTOM_MSG=Enter custom commit message (or press Enter to use default): 

if not "%CUSTOM_MSG%"=="" (
    set COMMIT_MSG=%CUSTOM_MSG%
)

echo.
echo 💾 Committing changes with message: "%COMMIT_MSG%"
git commit -m "%COMMIT_MSG%"
if errorlevel 1 (
    echo ❌ Failed to commit changes
    pause
    exit /b 1
)

REM Push to remote repository
echo.
echo 🚀 Pushing to remote repository...
git push origin main
if errorlevel 1 (
    echo ❌ Failed to push changes
    echo This might be due to network issues or authentication problems
    pause
    exit /b 1
)

echo.
echo ✅ SUCCESS: All changes have been automatically committed and pushed!
echo 🎉 Repository is now up to date
echo.
pause
