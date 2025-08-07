# PowerShell Auto-Commit Script for Auto DevOps Assistant
# This script provides more advanced auto-commit functionality

param(
    [string]$Message = "",
    [switch]$Watch = $false,
    [int]$WatchInterval = 30
)

Write-Host "🚀 Auto DevOps Assistant - PowerShell Auto-Commit" -ForegroundColor Cyan
Write-Host "======================================================" -ForegroundColor Cyan

# Function to check and commit changes
function Invoke-AutoCommit {
    param([string]$CommitMessage = "")
    
    # Check if we're in the right directory
    if (-not (Test-Path "backend\app.py")) {
        Write-Host "❌ Error: Not in the correct directory" -ForegroundColor Red
        Write-Host "Please run this script from the auto-devops-assistant root folder" -ForegroundColor Red
        return $false
    }
    
    # Check for changes
    $changes = git status --porcelain
    if (-not $changes) {
        Write-Host "✅ No changes detected - repository is clean" -ForegroundColor Green
        return $true
    }
    
    Write-Host "📝 Changes detected! Processing auto-commit..." -ForegroundColor Yellow
    
    # Display changes
    Write-Host "`n📋 Files changed:" -ForegroundColor Blue
    git status --short
    
    # Stage changes
    Write-Host "`n📦 Staging changes..." -ForegroundColor Blue
    git add .
    
    # Generate commit message if not provided
    if (-not $CommitMessage) {
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        $CommitMessage = "🔄 Auto-commit: Updates at $timestamp"
    }
    
    # Commit changes
    Write-Host "💾 Committing with message: '$CommitMessage'" -ForegroundColor Blue
    git commit -m $CommitMessage
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to commit changes" -ForegroundColor Red
        return $false
    }
    
    # Push changes
    Write-Host "🚀 Pushing to remote repository..." -ForegroundColor Blue
    git push origin main
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ SUCCESS: Changes committed and pushed!" -ForegroundColor Green
        return $true
    } else {
        Write-Host "❌ Failed to push changes" -ForegroundColor Red
        return $false
    }
}

# Function for watch mode
function Start-WatchMode {
    param([int]$Interval)
    
    Write-Host "`n👀 Starting watch mode - checking for changes every $Interval seconds" -ForegroundColor Magenta
    Write-Host "Press Ctrl+C to stop watching" -ForegroundColor Yellow
    
    try {
        while ($true) {
            $timestamp = Get-Date -Format "HH:mm:ss"
            Write-Host "[$timestamp] Checking for changes..." -ForegroundColor Gray
            
            Invoke-AutoCommit
            
            Start-Sleep -Seconds $Interval
        }
    }
    catch {
        Write-Host "`n👋 Watch mode stopped" -ForegroundColor Yellow
    }
}

# Main execution
if ($Watch) {
    Start-WatchMode -Interval $WatchInterval
} else {
    Invoke-AutoCommit -CommitMessage $Message
    Write-Host "`n💡 Tip: Use -Watch flag to automatically monitor and commit changes" -ForegroundColor Cyan
    Write-Host "Example: .\auto-commit.ps1 -Watch -WatchInterval 60" -ForegroundColor Cyan
}

Write-Host "`n🎉 Auto-commit script completed!" -ForegroundColor Green
