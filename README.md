# Auto DevOps Assistant

An **AI-powered agent** that helps DevOps engineers debug and fix deployment errors faster by analyzing deployment logs, detecting common issues, and recommending intelligent fixes using advanced pattern recognition and OpenAI GPT integration.

## 🎯 What It Does

- **🤖 AI-Powered Analysis** - Uses OpenAI GPT-3.5 for intelligent log interpretation
- **🔍 Pattern Recognition** - Advanced regex-based error detection
- **🎯 Smart Solutions** - Context-aware fix recommendations with code snippets
- **📊 Confidence Scoring** - AI provides reliability metrics for analysis
- **🚀 Auto-Detection** - Automatically identifies log sources and error types
- **💾 TiDB Integration** - Leverages TiDB Serverless for scalable log storage
- **🔄 Fallback System** - Works perfectly even without AI (demo mode)

## 🏗️ Architecture

```
Auto DevOps Assistant/
│
├── backend/                 # Flask API server with AI integration
│   ├── app.py              # Main Flask application with AI endpoints
│   ├── ai_service.py       # AI-powered log analysis service
│   ├── config.py           # Configuration (TiDB, OpenAI)
│   ├── requirements.txt    # Python dependencies including OpenAI
│   └── log_parser/         # Pattern-based log analysis
│       ├── __init__.py
│       └── parser.py       # Fallback analysis logic
│
├── frontend/               # Professional UI with AI features
│   ├── index.html          # Enhanced interface with AI indicators
│   ├── script.js           # AI-enhanced frontend logic
│   └── README.md           # Frontend documentation
│
├── AI_SETUP.md            # Complete AI setup guide
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

✅ **Phase 3: AI Integration** 
- OpenAI GPT-3.5 integration for intelligent analysis
- Advanced pattern recognition system
- Smart solution generation with confidence scoring
- Fallback system for reliable operation

✅ **Phase 4: Professional Frontend**
- Modern, responsive UI with Bootstrap 5
- AI-enhanced loading animations and progress tracking
- Real-time status indicators and confidence display
- Copy-to-clipboard functionality and downloadable reports

🔄 **Phase 5: Vector Search & Learning** (Next)
- TiDB vector search for similar issue detection
- Machine learning for pattern improvement
- Historical analysis and trend identification

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

The application includes an advanced demo mode that works without any configuration:
- **🤖 AI-Powered Analysis** - Experience intelligent log analysis
- **📋 Sample Error Logs** - Pre-loaded YAML, Docker, Kubernetes examples
- **💡 Smart Suggestions** - See AI-generated fix recommendations with confidence scores
- **🎯 Interactive UI** - Professional interface with loading animations
- **📊 Real-time Insights** - Pattern detection and solution ranking
- **🎪 Perfect for Hackathons** - Impressive demonstrations without setup

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

### Core Endpoints
- `GET /` - Professional frontend interface
- `GET /health` - System and database connectivity check  
- `POST /api/upload-log` - Standard log analysis with pattern recognition

### AI-Enhanced Endpoints  
- `POST /api/analyze-ai` - Advanced AI-powered log analysis
- `GET /api/ai-status` - Check AI service availability and capabilities

### Data Endpoints
- `GET /api/logs` - Retrieve stored analysis results
- `GET /api/fixes` - Get solution recommendations database

## 🎖️ TiDB AgentX Hackathon

This project is built for the TiDB AgentX Hackathon, showcasing:
- **🤖 AI-Powered Intelligence** - OpenAI GPT-3.5 integration for advanced log analysis
- **💾 TiDB Serverless** - Scalable cloud database for log storage and analytics
- **🔍 Vector Search** - Intelligent similarity matching for historical issue patterns  
- **🤝 Multi-Agent AI** - Coordinated AI agents for comprehensive DevOps automation
- **🌐 Real-world Application** - Solves actual DevOps pain points with production-ready solutions
- **🎯 Demo Excellence** - Professional interface with impressive AI capabilities

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

**Status**: ✅ **AI-Powered & Hackathon Ready** - Professional UI with Advanced AI Integration Complete
