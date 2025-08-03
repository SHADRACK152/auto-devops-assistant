# Run Instructions - Auto DevOps Assistant

## Quick Start (2 minutes)

### Prerequisites
- Python 3.8+
- Modern web browser
- Internet connection (for AI analysis)

### 1. Backend Setup
```bash
cd backend
pip install -r requirements.txt
python app.py
```
**Expected Output**: Server running on http://127.0.0.1:5000

### 2. Frontend Access
```bash
# Open in browser
frontend/index.html
```

### 3. Test the Demo
1. **Paste sample log**:
   ```
   [ERROR] Failed to connect to database: timeout expired
   [ERROR] ENV variable DATABASE_URL not set
   ```

2. **Select source**: Kubernetes

3. **Click**: "Analyze with AI"

4. **Expected Result**: 
   - 8 issues detected (5 critical)
   - 10 kubectl solutions with copy buttons
   - Learning feedback system

---

## Demo Features to Showcase

### **Multi-Step AI Workflow**
- ✅ Log analysis with pattern recognition
- ✅ TiDB vector search (with mock fallback)
- ✅ Groq AI analysis (with enhanced patterns fallback)
- ✅ kubectl command generation
- ✅ Solution effectiveness tracking

### **TiDB Integration Points**
- Vector search for similar deployment patterns
- Historical solution storage and retrieval  
- User feedback tracking for continuous learning
- Pattern effectiveness analytics

### **Real-World Solutions**
- Database connectivity troubleshooting
- Environment variable configuration
- Resource scaling recommendations
- Pod lifecycle management

---

## Troubleshooting

### Backend Issues
- **Port 5000 in use**: Change port in `app.py` line with `app.run()`
- **Missing dependencies**: Run `pip install flask flask-cors requests python-dotenv`
- **TiDB connection**: Uses mock database automatically if TiDB unavailable

### Frontend Issues  
- **CORS errors**: Ensure backend is running first
- **No solutions showing**: Check browser console for API errors
- **Styles missing**: Ensure `styles.css` is in same directory

---

## Environment Variables (Optional)

Create `backend/.env` for full AI features:
```bash
GROQ_API_KEY=your_groq_key_here
TIDB_HOST=gateway01.us-west-2.prod.aws.tidbcloud.com
TIDB_PORT=4000  
TIDB_USER=your_user
TIDB_PASSWORD=your_password
TIDB_DATABASE=auto_devops
```

**Note**: Demo works without these - uses intelligent fallbacks

---

## Demo Script (for judges)

1. **Start backend** (`python app.py`)
2. **Open frontend** (index.html in browser)  
3. **Paste deployment log** (use provided sample)
4. **Show results**: Issues detected + kubectl solutions
5. **Demonstrate learning**: Click feedback buttons
6. **Highlight TiDB**: Mention vector search and pattern storage

**Demo Time**: 3-5 minutes for full walkthrough

---

## Architecture Overview

```
Frontend (HTML/JS) → Flask API → TiDB Vector Search
                              ↓
                    Groq AI Analysis ← Pattern Matching
                              ↓
                    kubectl Solutions → User Feedback → TiDB Learning
```

**Key Innovation**: Multi-step agentic AI that learns from deployment patterns stored in TiDB Serverless to provide better troubleshooting over time.
