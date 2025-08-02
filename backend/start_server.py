#!/usr/bin/env python3
"""
Simple test script to verify installation and start the Flask server
"""

try:
    print("Testing imports...")
    import flask
    print(f"✓ Flask {flask.__version__} imported")
    
    import sqlalchemy
    print(f"✓ SQLAlchemy {sqlalchemy.__version__} imported")
    
    import pymysql
    print(f"✓ PyMySQL {pymysql.__version__} imported")
    
    from flask_cors import CORS
    print("✓ Flask-CORS imported")
    
    print("\nAll dependencies installed successfully!")
    print("Starting Flask server...")
    
    # Import and run our app
    from app import app
    print("✓ App imported successfully")
    
    if __name__ == '__main__':
        print("\n🚀 Starting Auto DevOps Assistant server...")
        print("📱 Frontend: http://127.0.0.1:5000/frontend")
        print("🔗 API: http://127.0.0.1:5000/health")
        print("Press Ctrl+C to stop the server\n")
        app.run(debug=True, host='127.0.0.1', port=5000)
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please run: pip install -r requirements.txt")
except Exception as e:
    print(f"❌ Error: {e}")
