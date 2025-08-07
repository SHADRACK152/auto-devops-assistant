# 🔄 Auto-Commit Setup for Auto DevOps Assistant

This directory contains scripts and configurations for automatically committing changes to your repository.

## 📝 Available Methods

### 1. **Batch Script (Windows)** - `auto-commit.bat`
```bash
# Run once to commit current changes
auto-commit.bat
```

**Features:**
- ✅ Checks for changes automatically
- ✅ Stages all files
- ✅ Creates timestamped commit messages
- ✅ Allows custom commit messages
- ✅ Pushes to remote repository
- ✅ Error handling and user feedback

### 2. **PowerShell Script** - `auto-commit.ps1`
```powershell
# Basic usage
.\auto-commit.ps1

# With custom message
.\auto-commit.ps1 -Message "🚀 Added new features"

# Watch mode (auto-commit every 30 seconds)
.\auto-commit.ps1 -Watch -WatchInterval 30
```

**Features:**
- ✅ All batch script features
- ✅ **Watch Mode**: Automatically monitors for changes
- ✅ Configurable check intervals
- ✅ Better error handling
- ✅ Colored output

### 3. **VS Code Integration**
Open Command Palette (`Ctrl+Shift+P`) and run:
- **"Tasks: Run Task"** → **"Auto Commit All Changes"**
- **"Tasks: Run Task"** → **"Start Auto-Commit Watch Mode"**

### 4. **Git Hooks** (Automatic)
The `post-commit` hook automatically pushes changes after every commit.

## 🚀 Quick Start

1. **One-time commit:**
   ```bash
   auto-commit.bat
   ```

2. **Automatic monitoring:**
   ```powershell
   .\auto-commit.ps1 -Watch
   ```

3. **VS Code Task:**
   - Press `Ctrl+Shift+P`
   - Type "Tasks: Run Task"
   - Select "Start Auto-Commit Watch Mode"

## ⚙️ Configuration

### Watch Mode Settings
- **Default interval**: 30 seconds
- **Custom interval**: Use `-WatchInterval <seconds>`
- **Stop watching**: Press `Ctrl+C`

### VS Code Auto-Save
The `.vscode/settings.json` enables:
- Auto-save after 1 second
- Smart Git commits
- Automatic Git fetch
- Recommended Git extensions

## 🎯 Best Practices

1. **Use descriptive commit messages:**
   ```powershell
   .\auto-commit.ps1 -Message "🔧 Fixed AWS Security Group patterns"
   ```

2. **Watch mode for active development:**
   ```powershell
   .\auto-commit.ps1 -Watch -WatchInterval 60
   ```

3. **Manual commits for important changes:**
   ```bash
   git add .
   git commit -m "🎉 Major milestone: Complete AI pattern system"
   git push origin main
   ```

## 🛡️ Safety Features

- ✅ **Change detection**: Only commits when files have changed
- ✅ **Error handling**: Stops on Git errors
- ✅ **Status reporting**: Clear success/failure messages
- ✅ **Directory validation**: Ensures you're in the correct project folder

## 💡 Tips

- **For hackathons**: Use watch mode to never lose changes
- **For development**: Use manual commits with descriptive messages
- **For demos**: Ensure all changes are committed before presenting

---

**Happy coding! 🚀** Your changes will never be lost again!
