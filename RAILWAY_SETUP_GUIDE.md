# 🚀 Railway Environment Variables Setup Guide

## How to Set Environment Variables in Railway Dashboard

1. **Go to Railway Dashboard**: https://railway.app/dashboard
2. **Select your project**: `auto-devops-assistant`
3. **Click on "Variables" tab**
4. **Add each variable below by clicking "Add"**

## Required Environment Variables

### 🤖 AI Configuration
- **Variable Name**: `GROQ_API_KEY`
- **Variable Value**: `[Your Groq API Key Here]`

### 🗄️ Database Configuration
- **Variable Name**: `TIDB_HOST`
- **Variable Value**: `[Your TiDB Host]`

- **Variable Name**: `TIDB_PORT`
- **Variable Value**: `4000`

- **Variable Name**: `TIDB_USER`
- **Variable Value**: `[Your TiDB Username]`

- **Variable Name**: `TIDB_PASSWORD`
- **Variable Value**: `[Your TiDB Password]`

- **Variable Name**: `TIDB_DATABASE`
- **Variable Value**: `test`

### ⚙️ Flask Configuration (Optional)
- **Variable Name**: `FLASK_ENV`
- **Variable Value**: `production`

- **Variable Name**: `PORT`
- **Variable Value**: `5000`

## After Adding Variables

1. Railway will automatically **redeploy** your application
2. Wait **2-3 minutes** for deployment to complete
3. **Test your application** - AI analysis should now work!

## Security Notes

- ✅ **Never commit API keys** to your repository
- ✅ **Use Railway Variables** for all sensitive data
- ✅ **Environment variables are encrypted** and secure in Railway
