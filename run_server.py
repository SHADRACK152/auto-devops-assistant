#!/usr/bin/env python3
"""
Auto DevOps Assistant - Simple Server Starter
This script starts the server from the project root directory.
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    print("🤖 Auto DevOps Assistant - TiDB AgentX Hackathon")
    print("=" * 50)
    
    # Get the project directories
    project_root = Path(__file__).parent
    backend_dir = project_root / "backend"
    
    print(f"📁 Project root: {project_root}")
    print(f"🔧 Backend dir: {backend_dir}")
    
    # Check if backend directory exists
    if not backend_dir.exists():
        print("❌ Backend directory not found!")
        return 1
    
    # Check if app.py exists
    app_file = backend_dir / "app.py"
    if not app_file.exists():
        print("❌ app.py not found in backend directory!")
        return 1
    
    print("\n🚀 Starting Auto DevOps Assistant Server...")
    print("-" * 50)
    print("🌐 Server will be available at:")
    print("  📱 Frontend: http://127.0.0.1:5000/")
    print("  🔗 API Health: http://127.0.0.1:5000/health")
    print("  📊 API Analyze: http://127.0.0.1:5000/api/upload-log")
    print("\n💡 Tips:")
    print("  • Open the frontend URL in your browser")
    print("  • Use Ctrl+C to stop the server")
    print("\n" + "=" * 50)
    print("🎯 Auto DevOps Assistant is starting...")
    print("=" * 50 + "\n")
    
    try:
        # Change to backend directory and run the app
        os.chdir(backend_dir)
        
        # Run the Flask app directly
        result = subprocess.run([
            sys.executable, "app.py"
        ], check=False)
        
        return result.returncode
        
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
        return 0
    except Exception as e:
        print(f"\n❌ Failed to start server: {e}")
        print("\nTroubleshooting:")
        print("1. Check if port 5000 is already in use")
        print("2. Verify dependencies: cd backend && pip install -r requirements.txt")
        print("3. Check if Python path is correct")
        return 1

if __name__ == '__main__':
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
