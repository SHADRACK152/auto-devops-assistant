# Auto DevOps Assistant Frontend

A modern, responsive web interface for the Auto DevOps Assistant.

## Features

- 🎨 **Modern UI** - Clean, professional design with Bootstrap 5
- 📱 **Responsive** - Works on desktop, tablet, and mobile
- 🚀 **Real-time Analysis** - Upload logs and get instant AI-powered insights
- 🔍 **Error Detection** - Automatically identifies deployment issues
- 💡 **Smart Suggestions** - AI-generated fix recommendations
- 📋 **Sample Logs** - Pre-loaded examples for quick testing
- 🎯 **One-Click Fixes** - Copy suggested code snippets

## Usage

### Option 1: Serve through Flask Backend
1. Start the Flask backend: `python app.py`
2. Visit: http://127.0.0.1:5000/frontend

### Option 2: Open Directly
1. Make sure Flask backend is running on port 5000
2. Open `index.html` in your browser
3. The frontend will connect to the API automatically

## Supported Log Types

- **Docker** - Container deployment errors, port conflicts
- **Kubernetes** - Pod failures, validation errors  
- **CI/CD** - Pipeline failures, build errors
- **YAML** - Configuration syntax errors
- **Application** - Runtime errors and exceptions

## Demo Flow

1. **Load Sample Log** - Click "Load YAML Error" or "Load Docker Error"
2. **Analyze** - Click "Analyze Log" or press Ctrl+Enter
3. **Review Results** - See error analysis and AI suggestions
4. **Copy Fixes** - Use suggested code snippets

## Technical Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Bootstrap 5, Font Awesome icons
- **API**: RESTful calls to Flask backend
- **Features**: Real-time status, error handling, responsive design

## API Endpoints Used

- `GET /health` - System status check
- `POST /api/upload-log` - Log analysis
- `GET /api/logs` - Retrieve stored logs
- `GET /api/fixes` - Get fix suggestions

Perfect for hackathon demos and real-world deployment troubleshooting!
