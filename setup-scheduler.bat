@echo off
REM Create Windows Task Scheduler entry for auto-commits
REM This will run auto-commit every 5 minutes automatically

set TASK_NAME=AutoDevOpsAssistant-AutoCommit
set SCRIPT_PATH=%cd%\auto-commit.bat
set LOG_PATH=%cd%\auto-commit.log

echo 📅 Setting up Windows Task Scheduler for automatic commits
echo ================================================================

REM Delete existing task if it exists
schtasks /delete /tn "%TASK_NAME%" /f >nul 2>&1

REM Create new scheduled task
echo 📝 Creating scheduled task: %TASK_NAME%
schtasks /create /tn "%TASK_NAME%" /tr "\"%SCRIPT_PATH%\" >> \"%LOG_PATH%\" 2>&1" /sc minute /mo 5 /ru "SYSTEM" /rl highest /f

if errorlevel 1 (
    echo ❌ Failed to create scheduled task
    echo Try running as Administrator
    pause
    exit /b 1
)

echo ✅ SUCCESS: Scheduled task created!
echo.
echo 📋 Task Details:
echo    Name: %TASK_NAME%
echo    Frequency: Every 5 minutes
echo    Script: %SCRIPT_PATH%
echo    Log: %LOG_PATH%
echo.
echo 🎯 Your repository will now auto-commit changes every 5 minutes!
echo.
echo 💡 Management commands:
echo    View task: schtasks /query /tn "%TASK_NAME%"
echo    Delete task: schtasks /delete /tn "%TASK_NAME%" /f
echo    Run now: schtasks /run /tn "%TASK_NAME%"
echo.
pause
