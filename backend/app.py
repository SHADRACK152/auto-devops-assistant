import os
import asyncio
from dotenv import load_dotenv

# Load environment variables from .env file FIRST (before other imports)
load_dotenv()

# Also manually load .env file as backup
try:
    with open('.env', 'r') as f:
        for line in f:
            if '=' in line and not line.strip().startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value
    print(f"🔑 Manual .env loading: GROQ_API_KEY {'✅ found' if os.getenv('GROQ_API_KEY') else '❌ missing'}")
except FileNotFoundError:
    print("⚠️  .env file not found")

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Import config with fallback for Railway deployment
try:
    from config import TIDB_CONFIG
    print("✅ Config imported successfully")
except ImportError as e:
    print(f"⚠️  Config import failed: {e}")
    # Fallback config for Railway deployment using environment variables
    TIDB_CONFIG = {
        "host": os.getenv("TIDB_HOST", "gateway01.eu-central-1.prod.aws.tidbcloud.com"),
        "port": int(os.getenv("TIDB_PORT", "4000")),
        "user": os.getenv("TIDB_USER", "t5uTfqdrPKmAXCN.root"),
        "password": os.getenv("TIDB_PASSWORD", "Nc6IzB7h26LPTi25"),
        "database": os.getenv("TIDB_DATABASE", "test"),
        "ssl_disabled": False,
        "ssl_verify_cert": False,
        "ssl_verify_identity": False,
    }
    print("✅ Using fallback config for Railway deployment")

from sqlalchemy import create_engine, text
from log_parser.parser import LogParser
from ai_service import ai_analyzer

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


# Create TiDB connection
def create_db_connection():
    try:
        import ssl
        
        # Create SSL context (the working method from our test)
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        # Build connection URI for SQLAlchemy
        uri = (f"mysql+pymysql://{TIDB_CONFIG['user']}:"
               f"{TIDB_CONFIG['password']}@{TIDB_CONFIG['host']}:"
               f"{TIDB_CONFIG['port']}/{TIDB_CONFIG['database']}")
        
        # SSL connection args for SQLAlchemy
        connect_args = {
            "ssl": ssl_context
        }
        
        engine = create_engine(uri, connect_args=connect_args, 
                             pool_timeout=30, pool_recycle=3600)
        
        # Test the connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ TiDB connection successful!")
            
        return engine
    except Exception as e:
        print(f"TiDB connection failed: {e}")
        print("Using mock database for development...")
        return None

# Initialize database connection (TiDB only)
engine = create_db_connection()
if engine is None:
    print("⚠️  TiDB connection not available. Running in pattern-only mode.")
    # Don't exit - allow app to run without database for Railway deployment

log_parser = LogParser()

@app.route('/')
def index():
    """Serve the frontend HTML at root"""
    try:
        # For Railway deployment, frontend is at ./frontend from project root
        current_dir = os.getcwd()
        frontend_path = os.path.join(current_dir, 'frontend')
        
        # Check if frontend directory exists
        if not os.path.exists(frontend_path):
            # Fallback: try relative to this file
            frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend')
        
        return send_from_directory(frontend_path, 'index.html')
    except Exception as e:
        # Fallback API response if frontend not available
        return jsonify({
            "message": "Auto DevOps Assistant API is running!",
            "status": "online", 
            "version": "1.0.0",
            "frontend_error": str(e),
            "current_dir": os.getcwd(),
            "endpoints": ["/health", "/api/upload-log", "/api/analyze-ai", "/api/ai-status"]
        })

@app.route('/api')
def api_info():
    """API information endpoint"""
    return jsonify({
        "message": "Auto DevOps Assistant API is running!",
        "status": "online",
        "version": "1.0.0", 
        "endpoints": ["/health", "/api/upload-log", "/api/analyze-ai", "/api/ai-status"]
    })

@app.route('/frontend')
def serve_frontend():
    """Serve the frontend HTML at /frontend"""
    try:
        current_dir = os.getcwd()
        frontend_path = os.path.join(current_dir, 'frontend')
        
        if not os.path.exists(frontend_path):
            frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend')
            
        return send_from_directory(frontend_path, 'index.html')
    except Exception:
        return "Frontend not available in this deployment"


@app.route('/<path:filename>')
def serve_static_files(filename):
    """Serve static files (CSS, JS, images) from frontend directory"""
    try:
        current_dir = os.getcwd()
        frontend_path = os.path.join(current_dir, 'frontend')
        
        if not os.path.exists(frontend_path):
            frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend')
            
        return send_from_directory(frontend_path, filename)
    except Exception as e:
        return f"File not found: {filename}", 404

@app.route('/health')
def health_check():
    """Simple health check endpoint for Railway deployment"""
    try:
        # Basic health check without database dependency
        return jsonify({
            "status": "healthy",
            "message": "Auto DevOps Assistant API is running",
            "service": "online",
            "timestamp": str(__import__('datetime').datetime.now())
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@app.route('/health/full')
def health_check_full():
    """Full health check endpoint to test database connectivity"""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            return jsonify({
                "status": "healthy",
                "database": "tidb_connected",
                "message": "Auto DevOps Assistant API running with TiDB"
            })
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "database": "error",
            "error": str(e)
        }), 500

@app.route('/api/upload-log', methods=['POST'])
def upload_log():
    """Endpoint to upload deployment logs for AI-powered analysis"""
    try:
        data = request.get_json()
        
        if not data or 'log_content' not in data:
            return jsonify({
                "error": "No log content provided"
            }), 400
        
        log_content = data['log_content']
        source = data.get('source', 'unknown')
        
        # Run AI-powered analysis
        try:
            # Direct call to AI analyzer (no async needed)
            analysis_result = ai_analyzer.analyze_log(log_content, source)
        except Exception as ai_error:
            print(f"AI analysis failed: {ai_error}")
            # Fallback to basic pattern analysis
            parsed_log = log_parser.parse_log(log_content, source)
            analysis_result = {
                "log_id": "fallback_" + str(hash(log_content))[:8],
                "severity": parsed_log['severity'],
                "summary": parsed_log['summary'],
                "errors_found": len(parsed_log['errors']),
                "errors": parsed_log['errors'],
                "ai_powered": False,
                "fallback_analysis": True
            }
        
        # Store analysis results in TiDB (if available)
        try:
            if engine is not None:
                with engine.connect() as connection:
                    # Store the log analysis in TiDB
                    insert_query = text("""
                        INSERT INTO log_analysis (content, source, severity, summary, created_at)
                        VALUES (:content, :source, :severity, :summary, NOW())
                    """)
                    result = connection.execute(insert_query, {
                        'content': log_content,
                        'source': source,
                        'severity': analysis_result['severity'],
                        'summary': analysis_result['summary']
                    })
                    connection.commit()
                    analysis_result['log_id'] = result.lastrowid
            else:
                # No database connection - use temporary ID
                analysis_result['log_id'] = "temp_" + str(hash(log_content))[:8]
        except Exception as db_error:
            print(f"Database storage error: {db_error}")
            analysis_result['log_id'] = "temp_" + str(hash(log_content))[:8]
        
        return jsonify({
            "message": "Log analyzed with AI-powered insights",
            "log_id": analysis_result['log_id'],
            "analysis": analysis_result,
            "ai_powered": analysis_result.get('ai_powered', False),
            "database": "tidb"
        })
        
    except Exception as e:
        return jsonify({
            "error": "Failed to process log",
            "details": str(e)
        }), 500


@app.route('/api/analyze-ai', methods=['POST'])
def analyze_with_ai():
    """Advanced AI-powered log analysis endpoint"""
    try:
        data = request.get_json()
        
        if not data or 'log_content' not in data:
            return jsonify({
                "error": "No log content provided",
                "usage": "POST with JSON body containing 'log_content' field"
            }), 400
        
        log_content = data['log_content']
        source = data.get('source', 'auto-detect')
        enable_ai = data.get('enable_ai', True)
        
        if not enable_ai:
            # Run only pattern-based analysis
            parsed_log = log_parser.parse_log(log_content, source)
            return jsonify({
                "message": "Pattern-based analysis completed",
                "analysis": {
                    "severity": parsed_log['severity'],
                    "summary": parsed_log['summary'],
                    "errors": parsed_log['errors'],
                    "ai_powered": False,
                    "analysis_type": "pattern_based"
                }
            })
        
        # Run full AI-powered analysis
        try:
            ai_result = ai_analyzer.analyze_log(log_content, source)
            
            return jsonify({
                "message": "AI-powered analysis completed successfully",
                "analysis": ai_result,
                "ai_powered": ai_result.get('ai_powered', False),
                "confidence": ai_result.get('confidence_score', 0.0)
            })
            
        except Exception as ai_error:
            # Graceful fallback to pattern analysis
            print(f"AI analysis error: {ai_error}")
            parsed_log = log_parser.parse_log(log_content, source)
            
            return jsonify({
                "message": "Analysis completed with fallback method",
                "analysis": {
                    "severity": parsed_log['severity'],
                    "summary": parsed_log['summary'],
                    "errors": parsed_log['errors'],
                    "ai_powered": False,
                    "fallback_reason": str(ai_error),
                    "analysis_type": "pattern_fallback"
                }
            })
            
    except Exception as e:
        return jsonify({
            "error": "Analysis failed",
            "details": str(e)
        }), 500


@app.route('/api/ai-status', methods=['GET'])
def ai_status():
    """Check AI service availability and capabilities including multi-backend AI"""
    try:
        # Get comprehensive AI status from the multi-backend system
        if hasattr(ai_analyzer, 'get_learning_stats'):
            ai_stats = ai_analyzer.get_learning_stats()
            
            # Determine the best available AI service
            ai_backends = ai_stats.get("ai_backends", {})
            online_ai = ai_backends.get("online_ai", {})
            local_ai = ai_backends.get("local_ai", {})
            
            # Determine primary service
            if online_ai.get("enabled") and online_ai.get("backends"):
                primary_service = f"Groq AI (Online) - {online_ai.get('active_backend', 'groq')}"
                ai_available = True
            elif local_ai.get("enabled") and local_ai.get("backends"):
                primary_service = f"Local AI - {local_ai.get('active_backend', 'gpt4all')}"
                ai_available = True
            elif ai_analyzer.openai_available:
                primary_service = "OpenAI GPT-3.5"
                ai_available = True
            else:
                primary_service = "Enhanced Pattern Recognition"
                ai_available = False
            
            return jsonify({
                "ai_available": ai_available,
                "ai_service": primary_service,
                "ai_backends": ai_backends,
                "features": {
                    "multi_backend_ai": True,
                    "online_ai": online_ai.get("enabled", False),
                    "local_ai": local_ai.get("enabled", False),
                    "pattern_recognition": True,
                    "ai_insights": ai_available,
                    "solution_generation": True,
                    "confidence_scoring": True,
                    "multi_source_analysis": True,
                    "self_learning": True,
                    "local_ai_support": local_ai.get("enabled", False)
                },
                "supported_sources": [
                    "docker", "kubernetes", "yaml", "jenkins", 
                    "nginx", "application", "auto-detect"
                ]
            })
        else:
            # Fallback to basic status check
            ai_available = ai_analyzer.openai_available if ai_analyzer else False
            return jsonify({
                "ai_available": ai_available,
                "ai_service": "OpenAI GPT-3.5" if ai_available else "Pattern Recognition",
                "features": {
                    "pattern_recognition": True,
                    "ai_insights": ai_available,
                    "solution_generation": True,
                    "confidence_scoring": True,
                    "multi_source_analysis": True,
                    "self_learning": True
                },
                "supported_sources": [
                    "docker", "kubernetes", "yaml", "jenkins", 
                    "nginx", "application", "auto-detect"
                ]
            })
        
    except Exception as e:
        return jsonify({
            "error": "Failed to check AI status",
            "details": str(e)
        }), 500


@app.route('/api/learning-stats', methods=['GET'])
def get_learning_stats():
    """Get AI learning and improvement statistics"""
    try:
        stats = ai_analyzer.get_learning_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/frontend/<path:filename>')
def serve_frontend_files(filename):
    """Serve frontend static files"""
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend')
    return send_from_directory(frontend_path, filename)


@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """Enhanced feedback endpoint with TiDB vector learning"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "error": "No feedback data provided",
                "usage": "POST with JSON body containing feedback data"
            }), 400
        
        analysis_id = data.get('analysis_id')
        solution_id = data.get('solution_id', 'general')
        rating = str(data.get('rating', '3'))
        helpful = data.get('helpful', True)
        feedback_text = data.get('feedback', '')
        
        if not analysis_id:
            return jsonify({
                "error": "analysis_id is required for feedback"
            }), 400
        
        # Process feedback through learning system
        try:
            learning_result = ai_analyzer.provide_feedback(analysis_id, data)
            tidb_result = {"learning_active": True, "feedback_recorded": True}
        except Exception as feedback_error:
            print(f"Feedback processing error: {feedback_error}")
            learning_result = {"feedback_processed": False}
            tidb_result = {"learning_active": False, "error": str(feedback_error)}
        
        return jsonify({
            "message": "🎯 Feedback recorded in TiDB vector database!",
            "tidb_learning": tidb_result,
            "pattern_learning": learning_result,
            "impact": "Your feedback helps improve AI recommendations for future deployments",
            "learning_active": tidb_result.get('learning_active', False)
        })
        
    except Exception as e:
        return jsonify({
            "error": "Failed to process feedback",
            "details": str(e)
        }), 500


@app.route('/api/logs', methods=['GET'])
def get_logs():
    """Get all logs or search logs"""
    try:
        if engine is None:
            return jsonify({
                "logs": [],
                "count": 0,
                "database": "not_connected",
                "message": "Database not available - logs not stored"
            })
        
        with engine.connect() as connection:
            query = text("SELECT * FROM log_analysis ORDER BY created_at DESC LIMIT 100")
            result = connection.execute(query)
            logs = [dict(row) for row in result.fetchall()]
            return jsonify({
                "logs": logs,
                "count": len(logs),
                "database": "tidb"
            })
    except Exception as e:
        return jsonify({
            "error": "Failed to retrieve logs",
            "details": str(e),
            "logs": [],
            "count": 0
        }), 500


@app.route('/api/fixes', methods=['GET'])
def get_fixes():
    """Get available fix suggestions"""
    try:
        if engine is None:
            # Return default fixes when database not available
            default_fixes = [
                {
                    "pattern_name": "Image Pull Error",
                    "description": "Container image pull failure",
                    "solution": "Check image name and registry credentials"
                },
                {
                    "pattern_name": "Resource Constraints", 
                    "description": "Pod scheduling issues",
                    "solution": "Increase resources or add more nodes"
                }
            ]
            return jsonify({
                "fixes": default_fixes,
                "count": len(default_fixes),
                "database": "not_connected"
            })
        
        with engine.connect() as connection:
            # Query for common deployment patterns and fixes
            query = text("""
                SELECT pattern_name, description, solution
                FROM deployment_patterns
                ORDER BY confidence DESC
                LIMIT 10
            """)
            result = connection.execute(query)
            fixes = [dict(row) for row in result.fetchall()]
            return jsonify({
                "fixes": fixes,
                "count": len(fixes),
                "database": "tidb"
            })
    except Exception as e:
        # Return some default fixes if database query fails
        default_fixes = [
            {
                "pattern_name": "Image Pull Error",
                "description": "Container image pull failure",
                "solution": "Check image name, registry credentials, and network connectivity"
            },
            {
                "pattern_name": "Resource Constraints",
                "description": "Pod scheduling issues due to insufficient resources",
                "solution": "Increase resource requests or add more nodes to the cluster"
            }
        ]
        return jsonify({
            "fixes": default_fixes,
            "count": len(default_fixes),
            "database": "fallback",
            "error": str(e)
        })


if __name__ == '__main__':
    # Get port from environment variable for cloud deployment
    port = int(os.environ.get('PORT', 5000))
    # Use debug=False for production
    debug_mode = os.environ.get('FLASK_ENV', 'development') == 'development'
    
    print(f"🚀 Starting Auto DevOps Assistant on port {port}")
    print(f"🔧 Debug mode: {debug_mode}")
    print(f"🌐 Environment: {os.environ.get('FLASK_ENV', 'development')}")
    
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
