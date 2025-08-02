# Auto DevOps Assistant

An AI-powered agent that helps DevOps engineers debug and fix deployment errors faster by analyzing deployment logs, detecting common issues, and recommending fixes.

## 🎯 What It Does

- **Analyzes** deployment logs from Docker, Kubernetes, CI/CD pipelines
- **Detects** common deployment issues using pattern matching and AI
- **Suggests** concrete fixes and configuration updates
- **Learns** from similar past issues using vector search

## 🏗️ Architecture

```
Auto DevOps Assistant/
│
├── backend/                 # Flask API server
│   ├── app.py              # Main Flask application
│   ├── config.py           # Configuration (TiDB, OpenAI)
│   ├── requirements.txt    # Python dependencies
│   └── log_parser/         # Log parsing module
│       ├── __init__.py
│       └── parser.py       # Log analysis logic
│
├── frontend/               # React UI (coming next)
└── README.md              # This file
```

## 🚀 Current Progress

✅ **Phase 1: Project Setup**
- Git repository initialized
- Project structure created

✅ **Phase 2: Backend Setup** 
- Flask API server created
- TiDB connection configuration
- Log parser module implemented
- Virtual environment set up

🔄 **Phase 3: Database & Vector Search** (Next)
- Create TiDB tables for logs and embeddings
- Implement vector search functionality
- OpenAI integration for log analysis

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/SHADRACK152/auto-devops-assistant.git
cd auto-devops-assistant
```

2. Set up backend:
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

3. Configure TiDB connection in `backend/config.py`

## 🚀 Quick Start

### Option 1: Direct Backend Start (Recommended)
```bash
# From the project root directory
cd backend
python app.py
```

### Option 2: Windows Batch File
```bash
# Double-click start.bat or run from command prompt:
start.bat
```

### Option 3: Alternative Startup Scripts
```bash
# Using the run server script
python run_server.py

# Or the original startup script
python start_server.py
```

## 📱 Access the Application

Once the server is running, open your browser and navigate to:
- **Frontend UI**: http://127.0.0.1:5000/
- **API Health Check**: http://127.0.0.1:5000/health
- **API Documentation**: http://127.0.0.1:5000/api/upload-log

## 🎮 Demo Mode

The application includes a demo mode that works without backend configuration:
- Load sample error logs (YAML, Docker, Kubernetes)
- See AI-powered analysis and fix suggestions
- Perfect for hackathon demonstrations

4. Run the Flask server:
```bash
python app.py
```

## 🔧 Configuration

Update `backend/config.py` with your credentials:

```python
TIDB_CONFIG = {
    "host": "YOUR_TIDB_HOST",
    "port": 4000,
    "user": "YOUR_USER",
    "password": "YOUR_PASSWORD", 
    "database": "auto_devops",
}

OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"
```

## 📝 API Endpoints

- `GET /` - Health check
- `GET /health` - Database connectivity check  
- `POST /api/upload-log` - Upload logs for analysis

## 🎖️ TiDB AgentX Hackathon

This project is built for the TiDB AgentX Hackathon, showcasing:
- **TiDB Serverless** for scalable log storage
- **Vector Search** for finding similar deployment issues  
- **Multi-step AI Agents** for intelligent log analysis
- **Real-world DevOps** problem solving

## 🐛 Troubleshooting

### Common Issues:

**1. "No module named 'app'" or Import Errors**
```bash
# Use the direct backend approach instead:
cd backend
python app.py
```

**2. "python: can't open file 'start_server.py'"**
```bash
# Make sure you're in the project root directory
cd auto-devops-assistant
python start_server.py
```

**3. "ModuleNotFoundError: No module named 'flask'"**
```bash
# Install dependencies in the backend directory
cd backend
pip install -r requirements.txt
```

**4. "Port 5000 already in use"**
```bash
# Kill any process using port 5000
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F
```

**5. TiDB Connection Issues**
- Check your `backend/config.py` settings
- Verify TiDB credentials and network connectivity
- The app works in demo mode without TiDB

**6. Frontend Not Loading**
- Ensure you're accessing http://127.0.0.1:5000/ (not localhost)
- Check browser console for JavaScript errors
- Try refreshing the page

### Getting Help:
- Check the `/health` endpoint for server status
- Review terminal output for error messages
- Demo mode works offline for testing

---

**Status**: ✅ Ready for TiDB AgentX Hackathon - Professional UI Complete
