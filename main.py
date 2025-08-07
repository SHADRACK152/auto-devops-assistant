#!/usr/bin/env python3
# Railway entry point for Auto DevOps Assistant
import sys
import os

print("🚀 Starting Auto DevOps Assistant for Railway deployment...")

try:
    # Add backend directory to path
    backend_path = os.path.join(os.path.dirname(__file__), 'backend')
    sys.path.insert(0, backend_path)
    
    # Change to backend directory
    os.chdir(backend_path)
    print(f"✅ Working directory: {os.getcwd()}")
    
    # Import and run the Flask app
    from app import app
    print("✅ Flask app imported successfully")
    
    if __name__ == '__main__':
        port = int(os.environ.get('PORT', 5000))
        print(f"🌐 Starting server on port {port}")
        
        # Run with production settings
        app.run(
            host='0.0.0.0', 
            port=port,
            debug=False,
            threaded=True
        )
        
except Exception as e:
    print(f"❌ Failed to start app: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
