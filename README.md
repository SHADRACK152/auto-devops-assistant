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

---

**Status**: 🚧 In Development - Backend Phase Complete
