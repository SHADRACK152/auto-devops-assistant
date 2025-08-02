#!/usr/bin/env python3
"""
Auto DevOps Assistant - Main Server Startup Script
For TiDB AgentX Hackathon

This script starts the Flask backend server from the root directory.
"""

import os
import sys
from pathlib import Path


def main():
    print("🤖 Auto DevOps Assistant - TiDB AgentX Hackathon")
    print("=" * 50)
    
    # Get the project root directory
    project_root = Path(__file__).parent
    backend_dir = project_root / "backend"
    frontend_dir = project_root / "frontend"
    
    print(f"📁 Project root: {project_root}")
    print(f"🔧 Backend dir: {backend_dir}")
    print(f"🎨 Frontend dir: {frontend_dir}")
    
    # Check if backend directory exists
    if not backend_dir.exists():
        print("❌ Backend directory not found!")
        return 1
    
    # Check if app.py exists
    app_file = backend_dir / "app.py"
    if not app_file.exists():
        print("❌ app.py not found in backend directory!")
        return 1
    
    # Check if frontend files exist
    frontend_index = frontend_dir / "index.html"
    if not frontend_index.exists():
        print("⚠️  Warning: Frontend index.html not found!")
    
    print("\n🔍 Checking dependencies...")
    
    # Change to backend directory
    os.chdir(backend_dir)
    
    # Add backend directory to Python path
    sys.path.insert(0, str(backend_dir))
    
    try:
        # Test imports
        print("Testing Python dependencies...")
        
        import flask
        print(f"✓ Flask {flask.__version__}")
        
        import sqlalchemy
        print(f"✓ SQLAlchemy {sqlalchemy.__version__}")
        
        import pymysql
        print(f"✓ PyMySQL {pymysql.__version__}")
        
        try:
            from flask_cors import CORS  # noqa: F401
            print("✓ Flask-CORS")
        except ImportError:
            print("⚠️  Flask-CORS not found (optional)")
        
        print("\n✅ All dependencies are installed!")
        
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("\nTo install dependencies, run:")
        print("  cd backend")
        print("  pip install -r requirements.txt")
        return 1
    
    try:
        print("\n🚀 Starting Auto DevOps Assistant Server...")
        print("-" * 50)
        
        # Import the Flask app from the backend directory
        from app import app
        print("✓ Flask app loaded successfully")
        
        # Print server information
        print("\n🌐 Server URLs:")
        print("  📱 Frontend: http://127.0.0.1:5000/")
        print("  🔗 API Health: http://127.0.0.1:5000/health")
        print("  📊 API Analyze: http://127.0.0.1:5000/api/upload-log")
        print("\n💡 Tips:")
        print("  • Open the frontend URL in your browser")
        print("  • Use Ctrl+C to stop the server")
        print("  • Check /health endpoint to verify API is working")
        print("\n" + "=" * 50)
        print("🎯 Auto DevOps Assistant is ready for TiDB AgentX Hackathon!")
        print("=" * 50 + "\n")
        
        # Start the Flask development server
        app.run(
            debug=True,
            host='127.0.0.1',
            port=5000,
            use_reloader=True
        )
        
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        print("\nTroubleshooting:")
        print("1. Check if port 5000 is already in use")
        print("2. Verify all dependencies are installed")
        print("3. Check config.py settings")
        return 1


if __name__ == '__main__':
    try:
        exit_code = main()
        sys.exit(exit_code or 0)
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
        print("Thank you for using Auto DevOps Assistant!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
