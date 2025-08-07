#!/usr/bin/env python3
# Railway entry point for Auto DevOps Assistant
import sys
import os

print("🚀 Starting Auto DevOps Assistant for Railway deployment... v2")

try:
    # Add both root and backend to Python path
    root_path = os.path.dirname(__file__)
    backend_path = os.path.join(root_path, 'backend')
    
    sys.path.insert(0, root_path)
    sys.path.insert(0, backend_path)
    
    print(f"✅ Root directory: {root_path}")
    print(f"✅ Backend directory: {backend_path}")
    
    # Import the Flask app from backend
    sys.path.append(backend_path)
    from backend.app import app
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
    
    # Try alternative import
    try:
        print("🔄 Trying alternative import method...")
        os.chdir(os.path.join(os.path.dirname(__file__), 'backend'))
        from app import app
        print("✅ Alternative import successful")
        
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port, debug=False)
        
    except Exception as e2:
        print(f"❌ Alternative import also failed: {e2}")
        sys.exit(1)
