@echo off
REM Auto-Commit System Status Checker
echo 🔍 Auto-Commit System Status Check
echo =====================================

REM Check if we're in the right directory
if not exist "backend\app.py" (
    echo ❌ Error: Not in Auto DevOps Assistant directory
    echo Please run from the project root folder
    pause
    exit /b 1
)

echo.
echo 📋 System Status:
echo -----------------

REM Check Git status
echo 🔧 Git Repository Status:
git status --short
if errorlevel 1 (
    echo ❌ Git error detected
) else (
    echo ✅ Git repository is healthy
)

echo.
echo 📁 Auto-Commit Files:
if exist "auto-commit.bat" (
    echo ✅ auto-commit.bat - Present
) else (
    echo ❌ auto-commit.bat - Missing
)

if exist "auto-commit.ps1" (
    echo ✅ auto-commit.ps1 - Present
) else (
    echo ❌ auto-commit.ps1 - Missing
)

if exist ".vscode\settings.json" (
    echo ✅ VS Code settings - Present
) else (
    echo ❌ VS Code settings - Missing
)

if exist ".git\hooks\post-commit" (
    echo ✅ Git post-commit hook - Present
) else (
    echo ❌ Git post-commit hook - Missing
)

echo.
echo 📅 Windows Task Scheduler:
schtasks /query /tn "AutoDevOpsAssistant-AutoCommit" >nul 2>&1
if errorlevel 1 (
    echo ❌ Scheduled task - Not configured
    echo    Run setup-scheduler.bat to enable
) else (
    echo ✅ Scheduled task - Active
)

echo.
echo 🎯 Quick Actions:
echo -----------------
echo 1. Run auto-commit.bat - One-time commit
echo 2. Run setup-scheduler.bat - Enable automatic commits every 5 minutes
echo 3. Use PowerShell: .\auto-commit.ps1 -Watch - Real-time monitoring
echo 4. VS Code: Ctrl+Shift+P → Tasks: Run Task → Auto Commit All Changes
echo.

REM Check for uncommitted changes
echo 📝 Pending Changes:
git diff --stat
if errorlevel 1 (
    echo No changes detected
) 

echo.
echo 🚀 Auto-Commit System Status Complete!
pause
