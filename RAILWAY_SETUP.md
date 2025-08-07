# 🚀 Railway Environment Variables Setup

## Required Environment Variables

Set these in your Railway dashboard under **Variables** tab:

### 🤖 AI Configuration
```
GROQ_API_KEY=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
```

### 🗄️ Database Configuration
```
TIDB_HOST=gateway01.eu-central-1.prod.aws.tidbcloud.com
TIDB_PORT=4000
TIDB_USER=t5uTfqdrPKmAXCN.root
TIDB_PASSWORD=Nc6IzB7h26LPTi25
TIDB_DATABASE=test
```

### ⚙️ Application Configuration
```
FLASK_ENV=production
PORT=5000
```

## 📋 Setup Steps

1. **Access Railway Dashboard**: https://railway.app/dashboard
2. **Select Project**: `auto-devops-assistant`
3. **Go to Variables Tab**
4. **Add Each Variable** one by one using the format above
5. **Deploy**: Railway will automatically restart with new environment variables

## ✅ Verification

After setting variables, check these endpoints:
- **AI Status**: https://auto-devops-assistant-production.up.railway.app/api/ai-status
- **Health Check**: https://auto-devops-assistant-production.up.railway.app/health
- **Debug Environment**: https://auto-devops-assistant-production.up.railway.app/api/debug-env

## 🔐 Security Notes

- ✅ All sensitive data is stored as Railway environment variables
- ✅ No hardcoded credentials in source code
- ✅ Environment variables are encrypted at rest
- ✅ Variables are only accessible to your Railway project
