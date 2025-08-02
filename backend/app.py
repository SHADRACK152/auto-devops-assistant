from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from config import TIDB_CONFIG
from sqlalchemy import create_engine, text
from mock_db import get_mock_database
from log_parser.parser import LogParser
from ai_service_v2 import ai_analyzer
import os
import asyncio

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

# Initialize database connection (TiDB or mock)
engine = create_db_connection()
use_mock_db = engine is None
mock_db = get_mock_database() if use_mock_db else None
log_parser = LogParser()

@app.route('/')
def index():
    """Serve the frontend HTML at root"""
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend')
    return send_from_directory(frontend_path, 'index.html')

@app.route('/<path:filename>')
def serve_static_files(filename):
    """Serve static files (CSS, JS, images) from frontend directory"""
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend')
    return send_from_directory(frontend_path, filename)

@app.route('/health')
def health_check():
    """Health check endpoint to test database connectivity"""
    try:
        if use_mock_db:
            stats = mock_db.get_stats()
            return jsonify({
                "status": "healthy",
                "database": "mock_database",
                "message": "Auto DevOps Assistant API running with mock database",
                "stats": stats
            })
        else:
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
        
        # Store analysis results
        if use_mock_db:
            log_id = mock_db.add_log(
                content=log_content,
                source=source,
                severity=analysis_result['severity'],
                summary=analysis_result['summary']
            )
            analysis_result['log_id'] = log_id
        else:
            # TODO: Store in TiDB when connection is working
            pass
        
        return jsonify({
            "message": "Log analyzed with AI-powered insights",
            "log_id": analysis_result['log_id'],
            "analysis": analysis_result,
            "ai_powered": analysis_result.get('ai_powered', False),
            "database": "mock" if use_mock_db else "tidb"
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
    """Check AI service availability and capabilities"""
    try:
        # Check if AI analyzer is available
        ai_available = ai_analyzer.openai_available if ai_analyzer else False
        
        return jsonify({
            "ai_available": ai_available,
            "ai_service": "OpenAI GPT-3.5" if ai_available else "Pattern-based only",
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


@app.route('/api/feedback', methods=['POST'])
def provide_feedback():
    """Allow users to provide feedback on analysis accuracy"""
    try:
        data = request.get_json()
        
        if not data or 'log_id' not in data or 'pattern_type' not in data or 'helpful' not in data:
            return jsonify({
                "error": "Missing required fields: log_id, pattern_type, helpful"
            }), 400
        
        log_id = data['log_id']
        pattern_type = data['pattern_type']
        helpful = data['helpful']
        
        result = ai_analyzer.provide_feedback(log_id, pattern_type, helpful)
        
        return jsonify({
            "message": "Feedback recorded successfully",
            "result": result
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/learning-stats', methods=['GET'])
def get_learning_stats():
    """Get AI learning and improvement statistics"""
    try:
        stats = ai_analyzer.get_learning_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/frontend')
@app.route('/frontend/')
def serve_frontend():
    """Serve the frontend HTML"""
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend')
    return send_from_directory(frontend_path, 'index.html')


@app.route('/frontend/<path:filename>')
def serve_frontend_files(filename):
    """Serve frontend static files"""
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend')
    return send_from_directory(frontend_path, filename)


@app.route('/api/logs', methods=['GET'])
def get_logs():
    """Get all logs or search logs"""
    try:
        if use_mock_db:
            logs = mock_db.get_all_logs()
            return jsonify({
                "logs": logs,
                "count": len(logs),
                "database": "mock"
            })
        else:
            # TODO: Query TiDB when connection is working
            return jsonify({
                "logs": [],
                "count": 0,
                "database": "tidb",
                "message": "TiDB integration pending"
            })
    except Exception as e:
        return jsonify({
            "error": "Failed to retrieve logs",
            "details": str(e)
        }), 500


@app.route('/api/fixes', methods=['GET'])
def get_fixes():
    """Get available fix suggestions"""
    try:
        if use_mock_db:
            fixes = mock_db.get_fix_suggestions()
            return jsonify({
                "fixes": fixes,
                "count": len(fixes),
                "database": "mock"
            })
        else:
            # TODO: Query TiDB when connection is working
            return jsonify({
                "fixes": [],
                "count": 0,
                "database": "tidb",
                "message": "TiDB integration pending"
            })
    except Exception as e:
        return jsonify({
            "error": "Failed to retrieve fixes",
            "details": str(e)
        }), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
