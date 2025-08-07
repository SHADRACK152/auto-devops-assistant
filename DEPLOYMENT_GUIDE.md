# 🚀 Auto DevOps Assistant - Complete Deployment Guide

> **Repository**: https://github.com/SHADRACK152/auto-devops-assistant  
> **Branch**: main  
> **Live Demo**: https://shadrack152.github.io/auto-devops-assistant/

## 📋 Table of Contents

1. [Quick Deploy Options](#quick-deploy-options)
2. [Railway Deployment (Recommended)](#railway-deployment)
3. [Heroku Deployment](#heroku-deployment)
4. [Vercel Deployment](#vercel-deployment)
5. [DigitalOcean App Platform](#digitalocean-app-platform)
6. [GitHub Codespaces](#github-codespaces)
7. [Local Development](#local-development)
8. [Environment Variables Setup](#environment-variables-setup)
9. [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Deploy Options

| Platform | Deployment Time | Cost | Difficulty |
|----------|----------------|------|------------|
| **Railway** | 3 minutes | Free tier | ⭐ Easy |
| **Heroku** | 5 minutes | Free tier | ⭐⭐ Easy |
| **Vercel** | 2 minutes | Free tier | ⭐ Easy |
| **DigitalOcean** | 4 minutes | $5/month | ⭐⭐ Medium |

---

## 🛤️ Railway Deployment (Recommended)

### Step 1: Fork the Repository
1. Go to: https://github.com/SHADRACK152/auto-devops-assistant
2. Click **"Fork"** button (top right)
3. Select your GitHub account
4. Wait for fork to complete

### Step 2: Deploy to Railway
1. **Visit Railway**: https://railway.app/
2. **Sign up/Login** with GitHub
3. **Create New Project**:
   ```
   - Click "Deploy from GitHub repo"
   - Select "auto-devops-assistant" (your fork)
   - Click "Deploy Now"
   ```

### Step 3: Configure Environment Variables
1. **In Railway Dashboard**:
   - Go to your project
   - Click **"Variables"** tab
   - Add these variables:

   ```bash
   PORT=5000
   FLASK_ENV=production
   GROQ_API_KEY=your-groq-api-key-here
   ```

### Step 4: Get Your Groq API Key (FREE)
1. **Visit**: https://console.groq.com/
2. **Sign up** with Google/GitHub
3. **Go to API Keys** section
4. **Create new key**, copy it
5. **Paste in Railway** `GROQ_API_KEY` variable

### Step 5: Deploy
1. **Railway auto-deploys** from your GitHub repo
2. **Wait 2-3 minutes** for build completion
3. **Get your URL**: `https://your-project-name.railway.app`
4. **Test the app**: Your Auto DevOps Assistant is live! 🎉

---

## 🟣 Heroku Deployment

### Step 1: Fork Repository (Same as above)

### Step 2: Deploy to Heroku
1. **Visit**: https://heroku.com/
2. **Create account/Login**
3. **Create New App**:
   ```
   - Click "Create new app"
   - App name: "your-devops-assistant"
   - Region: United States (or Europe)
   - Click "Create app"
   ```

### Step 3: Connect GitHub
1. **In Heroku Dashboard**:
   - Go to "Deploy" tab
   - Select "GitHub" as deployment method
   - Connect your GitHub account
   - Search for "auto-devops-assistant"
   - Click "Connect"

### Step 4: Set Environment Variables
1. **Go to "Settings" tab**
2. **Click "Reveal Config Vars"**
3. **Add variables**:
   ```
   GROQ_API_KEY = your-groq-api-key-here
   FLASK_ENV = production
   ```

### Step 5: Deploy
1. **Go to "Deploy" tab**
2. **Manual Deploy section**
3. **Select branch**: main
4. **Click "Deploy Branch"**
5. **Wait for build** (3-5 minutes)
6. **Click "View"** - Your app is live!

---

## ▲ Vercel Deployment (Frontend Only)

### Step 1: Fork Repository

### Step 2: Deploy Frontend
1. **Visit**: https://vercel.com/
2. **Sign up with GitHub**
3. **New Project**:
   ```
   - Click "Add New Project"
   - Import "auto-devops-assistant"
   - Root Directory: "frontend"
   - Framework: "Static HTML"
   - Click "Deploy"
   ```

### Step 3: Backend on Railway
- **Frontend**: Deployed on Vercel (static files)
- **Backend**: Deploy on Railway (API server)
- **Update**: Modify frontend to point to Railway backend URL

---

## 🌊 DigitalOcean App Platform

### Step 1: Fork Repository

### Step 2: Create App
1. **Visit**: https://cloud.digitalocean.com/apps
2. **Create App** → **GitHub**
3. **Configure**:
   ```
   Repository: auto-devops-assistant
   Branch: main
   Source Directory: /backend
   ```

### Step 3: App Settings
```yaml
Name: auto-devops-assistant
Region: New York
Plan: Basic ($5/month)
Environment Variables:
  - GROQ_API_KEY=your-groq-api-key-here
  - FLASK_ENV=production
  - PORT=8080
Build Command: pip install -r requirements.txt
Run Command: python app.py
```

### Step 4: Deploy
1. **Review settings**
2. **Click "Create Resources"**
3. **Wait 5-10 minutes**
4. **Get your app URL**

---

## 💻 GitHub Codespaces (Development)

### Step 1: Open in Codespaces
1. **Go to your forked repo**
2. **Click "Code" button**
3. **Select "Codespaces" tab**
4. **Click "Create codespace on main"**
5. **Wait for environment setup**

### Step 2: Setup Environment
```bash
# In Codespaces terminal
cd backend
pip install -r requirements.txt

# Create .env file
echo "GROQ_API_KEY=your-groq-api-key-here" > .env
echo "FLASK_ENV=development" >> .env
```

### Step 3: Run Application
```bash
# Start backend
python app.py

# Open another terminal for frontend
cd ../frontend
python -m http.server 3000
```

### Step 4: Access Application
- **Backend**: Port 5000 (auto-forwarded)
- **Frontend**: Port 3000 (auto-forwarded)
- **Full App**: Click the forwarded URL

---

## 🛠️ Local Development

### Prerequisites
```bash
- Python 3.8+
- Git
- A web browser
```

### Step 1: Clone Repository
```bash
git clone https://github.com/SHADRACK152/auto-devops-assistant.git
cd auto-devops-assistant
```

### Step 2: Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Environment Variables
```bash
# Create .env file in backend folder
echo "GROQ_API_KEY=your-groq-api-key-here" > .env
echo "FLASK_ENV=development" >> .env
```

### Step 4: Run Application
```bash
# Start backend server
python app.py

# Open new terminal for frontend
cd ../frontend
python -m http.server 3000
# OR if you have Node.js:
npx serve .
```

### Step 5: Access Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **Test**: Upload a log file and see AI analysis!

---

## 🔑 Environment Variables Setup

### Required Variables
```bash
GROQ_API_KEY=gsk_xxxxxxxxxxxx    # Get from console.groq.com (FREE)
```

### Optional Variables
```bash
FLASK_ENV=production             # production or development
PORT=5000                        # Server port (auto-set by platforms)
OPENAI_API_KEY=sk_xxxxxxxxxxxx   # OpenAI API (if you have credits)
DEBUG=False                      # Enable debug mode
```

### Getting Free API Keys

#### 🚀 Groq (Recommended - FREE)
1. **Visit**: https://console.groq.com/
2. **Sign up** with Google/GitHub
3. **Go to "API Keys"**
4. **Create New Secret Key**
5. **Copy the key** (starts with `gsk_`)
6. **Use in your deployment**

#### 🤖 OpenAI (Optional - Paid)
1. **Visit**: https://platform.openai.com/
2. **Create account**
3. **Add payment method** ($5 minimum)
4. **Go to API Keys**
5. **Create new key**

---

## 🔧 Troubleshooting

### Common Issues

#### ❌ "Module not found" Error
```bash
# Solution: Install missing packages
pip install -r backend/requirements.txt
```

#### ❌ "API Key not found" Error
```bash
# Solution: Check environment variables
# Make sure GROQ_API_KEY is set correctly
```

#### ❌ "Port already in use"
```bash
# Solution: Change port or kill process
# Windows:
netstat -ano | findstr :5000
taskkill /PID <process_id> /F

# macOS/Linux:
lsof -ti:5000 | xargs kill -9
```

#### ❌ "Database connection failed"
```bash
# Solution: TiDB is pre-configured
# Check your internet connection
# The app works without database (fallback mode)
```

### Platform-Specific Issues

#### Railway
- **Build fails**: Check `railway.toml` configuration
- **App crashes**: Check environment variables
- **Slow response**: Check if app is sleeping (free tier)

#### Heroku
- **Build timeout**: Use smaller dependencies
- **Memory limit**: Optimize Python imports
- **Dyno sleeping**: Upgrade to paid plan or use uptimerobot

#### Vercel
- **Function timeout**: Vercel has 10s limit for free tier
- **Large files**: Use Railway for backend instead

---

## 🎯 Post-Deployment Checklist

### ✅ Test Your Deployment
1. **Visit your app URL**
2. **Upload a sample log file**:
   ```
   Sample Docker error log:
   ERROR: Failed to start container
   docker: Error response from daemon: driver failed programming external connectivity
   ```
3. **Check AI analysis response**
4. **Verify all features work**

### ✅ Monitor Your App
- **Railway**: Built-in monitoring dashboard
- **Heroku**: Use Heroku metrics or New Relic
- **Vercel**: Analytics dashboard
- **DigitalOcean**: App monitoring panel

### ✅ Set Up Alerts
```bash
# Use these services for uptime monitoring:
- UptimeRobot (free)
- Pingdom
- StatusCake
```

### ✅ Custom Domain (Optional)
1. **Purchase domain** (Namecheap, GoDaddy)
2. **Configure DNS** in platform settings
3. **Enable SSL** (auto-configured)

---

## 🚀 Advanced Deployment Options

### Docker Deployment
```dockerfile
# Dockerfile (already in repo)
FROM python:3.9-slim
WORKDIR /app
COPY backend/ .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]
```

### Kubernetes Deployment
```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: auto-devops-assistant
spec:
  replicas: 3
  selector:
    matchLabels:
      app: auto-devops-assistant
  template:
    metadata:
      labels:
        app: auto-devops-assistant
    spec:
      containers:
      - name: app
        image: your-registry/auto-devops-assistant
        ports:
        - containerPort: 5000
        env:
        - name: GROQ_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-keys
              key: groq-api-key
```

### AWS EC2 Deployment
```bash
# Launch EC2 instance
# Connect via SSH
sudo apt update
sudo apt install python3-pip git

# Clone and setup
git clone https://github.com/SHADRACK152/auto-devops-assistant.git
cd auto-devops-assistant/backend
pip3 install -r requirements.txt

# Create .env file
echo "GROQ_API_KEY=your-key-here" > .env

# Run with nohup
nohup python3 app.py &

# Configure reverse proxy (Nginx)
sudo apt install nginx
# Configure nginx to proxy :80 to :5000
```

---

## 💡 Tips for Production

### Performance Optimization
```python
# In app.py, add:
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)

# Enable caching
from flask_caching import Cache
cache = Cache(app)
```

### Security Best Practices
```python
# Environment variables for sensitive data
import os
from dotenv import load_dotenv

load_dotenv()

# Never commit API keys to git
# Use .env files and .gitignore
# Rotate API keys regularly
```

### Scaling Considerations
- **Database**: Upgrade TiDB plan for high traffic
- **CDN**: Use CloudFlare for static assets
- **Load Balancer**: Multiple app instances
- **Caching**: Redis for API responses

---

## 📞 Support

### Need Help?
- **GitHub Issues**: https://github.com/SHADRACK152/auto-devops-assistant/issues
- **Documentation**: This guide + README.md
- **Demo**: https://shadrack152.github.io/auto-devops-assistant/

### Resources
- **Flask Documentation**: https://flask.palletsprojects.com/
- **Railway Docs**: https://docs.railway.app/
- **Heroku Docs**: https://devcenter.heroku.com/
- **Groq API Docs**: https://console.groq.com/docs

---

## 🎉 Conclusion

Your **Auto DevOps Assistant** is now ready for deployment! Choose the platform that best fits your needs:

- **Quick Demo**: Use Railway (3 minutes)
- **Production Ready**: Use DigitalOcean or AWS
- **Development**: Use GitHub Codespaces
- **Learning**: Use Local Development

**Remember**: The app works perfectly even without API keys thanks to the intelligent fallback system with pattern recognition!

---

**🚀 Happy Deploying!** 

*Made with ❤️ for the TiDB Hackathon 2025*
