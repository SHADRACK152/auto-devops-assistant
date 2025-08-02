from flask import Flask, request, jsonify
from config import TIDB_CONFIG
from sqlalchemy import create_engine, text
from mock_db import get_mock_database
from log_parser.parser import LogParser

app = Flask(__name__)


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
    return "Auto DevOps Assistant API is running"

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
    """Endpoint to upload deployment logs for analysis"""
    try:
        data = request.get_json()
        
        if not data or 'log_content' not in data:
            return jsonify({
                "error": "No log content provided"
            }), 400
        
        log_content = data['log_content']
        source = data.get('source', 'unknown')
        
        # Parse the log content
        parsed_log = log_parser.parse_log(log_content, source)
        
        if use_mock_db:
            # Store in mock database
            log_id = mock_db.add_log(
                content=log_content,
                source=source,
                severity=parsed_log['severity'],
                summary=parsed_log['summary']
            )
        else:
            # TODO: Store in TiDB when connection is working
            log_id = parsed_log['id']
        
        return jsonify({
            "message": "Log uploaded and analyzed successfully",
            "log_id": log_id,
            "analysis": {
                "severity": parsed_log['severity'],
                "errors_found": len(parsed_log['errors']),
                "summary": parsed_log['summary'],
                "errors": parsed_log['errors']
            },
            "database": "mock" if use_mock_db else "tidb"
        })
        
    except Exception as e:
        return jsonify({
            "error": "Failed to process log",
            "details": str(e)
        }), 500


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
