# Auto DevOps Assistant

An **AI-powered DevOps assistant** that helps engineers debug and fix deployment errors faster by analyzing deployment logs, detecting patterns, and providing single, comprehensive solutions using advanced pattern recognition and TiDB integration.

## 🎯 What It Does

- **🤖 Enhanced Pattern Recognition** - Advanced pattern detection with TiDB vector search
- **🎯 Single Solution Focus** - Provides one comprehensive, finalized solution per analysis
- **📊 Success Rate Tracking** - Monitors solution effectiveness and learns from outcomes
- **� TiDB Vector Storage** - Stores and retrieves patterns using TiDB vector similarity search
- **� Intelligent Classification** - Automatically categorizes Docker, Kubernetes, Database, and Network issues
- **🔄 Self-Learning System** - Continuously improves through pattern storage and feedback

## 🏗️ Architecture

```
Auto DevOps Assistant/
│
├── backend/                           # Flask API server with enhanced AI
│   ├── app.py                        # Main Flask application
│   ├── ai_service.py                 # Enhanced AI service with single solutions
│   ├── enhanced_pattern_recognition.py # TiDB-powered pattern recognition
│   ├── vector_search.py             # TiDB vector similarity search
│   ├── online_ai_service.py         # Groq AI integration
│   ├── config.py                    # Configuration (TiDB, Groq)
│   ├── requirements.txt             # Python dependencies
│   └── log_parser/                  # Legacy pattern analysis
│       ├── __init__.py
│       └── parser.py
│
├── frontend/                         # Professional UI
│   ├── index.html                   # Enhanced interface
│   ├── script.js                    # Frontend logic with single solution display
│   └── style.css                    # Application styling
│
└── README.md                        # This file
```

## ✅ Current Status

**Enhanced Pattern Recognition System**
- ✅ TiDB vector search integration for pattern similarity matching
- ✅ Single comprehensive solution architecture (no more scattered recommendations)
- ✅ Pattern-specific solvers for Docker, Kubernetes, Database, and Network issues
- ✅ Success rate tracking and continuous learning from user feedback
- ✅ Professional UI with step-by-step solution display

**Core Features Complete**
- ✅ Flask API server with enhanced AI integration
- ✅ TiDB Serverless database for pattern storage and retrieval
- ✅ Groq AI integration for intelligent analysis
- ✅ Modern responsive frontend with single solution focus
- ✅ Automatic issue classification and targeted solution generation

## � Quick Start

1. **Clone and Setup**
```bash
git clone https://github.com/SHADRACK152/auto-devops-assistant.git
cd auto-devops-assistant
```

2. **Backend Setup**
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows (use `source venv/bin/activate` on macOS/Linux)
pip install -r requirements.txt
```

> **Note**: The project has two requirements.txt files:
> - `requirements.txt` (root) - Used by Railway for deployment
> - `backend/requirements.txt` - For local development
> Both files are kept in sync for consistency.

3. **Environment Configuration**
Create a `.env` file in the `backend/` directory:
```env
GROQ_API_KEY=your_groq_api_key_here
TIDB_HOST=your_tidb_host
TIDB_PORT=4000
TIDB_USER=your_username
TIDB_PASSWORD=your_password
TIDB_DATABASE=auto_devops
```

4. **Start the Application**
```bash
python app.py
```

5. **Access the Application**
Open your browser to: http://127.0.0.1:5000/

## 🔧 Configuration

The application uses environment variables for configuration. Update your `.env` file in the `backend/` directory:

```env
# Groq AI Configuration
GROQ_API_KEY=your_groq_api_key_here

# TiDB Configuration  
TIDB_HOST=your_tidb_host
TIDB_PORT=4000
TIDB_USER=your_username
TIDB_PASSWORD=your_password
TIDB_DATABASE=auto_devops
```

## 📝 API Endpoints

### Core Endpoints
- `GET /` - Main application interface
- `GET /health` - System and database connectivity check  
- `POST /api/analyze` - Enhanced log analysis with single comprehensive solutions

### Data Endpoints
- `GET /api/logs` - Retrieve stored analysis results
- `GET /api/patterns` - Get pattern recognition statistics

## � Key Features

This DevOps assistant showcases:
- **🤖 Enhanced Pattern Recognition** - TiDB vector search for intelligent pattern matching
- **💾 TiDB Vector Storage** - Scalable pattern storage with similarity search capabilities
- **🎯 Single Solution Architecture** - Provides one comprehensive solution instead of scattered recommendations  
- **🔍 Intelligent Classification** - Automatically categorizes and solves Docker, Kubernetes, Database, and Network issues
- **📊 Success Tracking** - Monitors solution effectiveness and learns from user feedback
- **� Production-Ready** - Professional interface with real-world DevOps problem solving

## 🐛 Troubleshooting

### Common Issues:

**1. ModuleNotFoundError: No module named 'numpy'**
```bash
# For Railway deployment: Check root requirements.txt has numpy
# For local development: Install in backend directory
cd backend
pip install -r requirements.txt
```

**2. JavaScript Errors (Uncaught SyntaxError)**
```bash
# Clear browser cache and refresh the page
# Check browser developer console for specific errors
# Ensure script.js loads properly
```

**3. "analyzeLog is not defined" Error**
- This occurs when JavaScript fails to load due to syntax errors
- Clear browser cache and reload the page
- Check Network tab in developer tools to ensure script.js loads

**4. Statistics showing "0 Issues Found" despite having results**
- This was fixed in the latest version
- The UI now properly counts issues and solutions from enhanced format
- Refresh the application to see correct counts

**2. Module Import Errors**
```bash
# Ensure you're in the backend directory
cd backend
python app.py
```

**3. Missing Dependencies**
```bash
# Install all required packages
cd backend
pip install -r requirements.txt
```

**4. Port 5000 Already in Use**
```bash
# Windows: Kill process using port 5000
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F
```

**5. TiDB Connection Issues**
- Verify your `.env` file has correct TiDB credentials
- Check network connectivity to TiDB
- Ensure the `auto_devops` database exists

**6. Frontend Loading Issues**
- Access http://127.0.0.1:5000/ (not localhost)
- Check browser console for JavaScript errors
- Clear browser cache and refresh

### Getting Help:
- Check the `/health` endpoint for system status
- Review terminal output for detailed error messages
- Ensure all environment variables are properly set

---

**Status**: ✅ **Production Ready** - Enhanced Pattern Recognition with TiDB Integration Complete
