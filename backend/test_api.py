"""
Simple test script to verify Flask app and database connectivity
"""

import requests
import json
from config import TIDB_CONFIG

def test_flask_app():
    """Test if Flask app is running"""
    try:
        response = requests.get("http://127.0.0.1:5000/")
        if response.status_code == 200:
            print("✅ Flask app is running!")
            print(f"Response: {response.text}")
            return True
        else:
            print(f"❌ Flask app returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Flask app. Make sure it's running on port 5000.")
        return False
    except Exception as e:
        print(f"❌ Error testing Flask app: {e}")
        return False

def test_health_endpoint():
    """Test the health check endpoint"""
    try:
        response = requests.get("http://127.0.0.1:5000/health")
        if response.status_code == 200:
            data = response.json()
            print("✅ Health endpoint working!")
            print(f"Database status: {data.get('database', 'unknown')}")
            return True
        else:
            print(f"❌ Health endpoint returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing health endpoint: {e}")
        return False

def test_log_upload():
    """Test log upload functionality"""
    sample_log = """
ERROR: yaml.scanner.ScannerError: mapping values are not allowed here
  in "docker-compose.yml", line 5, column 13
"""
    
    try:
        response = requests.post(
            "http://127.0.0.1:5000/api/upload-log",
            json={
                "log_content": sample_log,
                "source": "docker"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Log upload endpoint working!")
            print(f"Response: {data}")
            return True
        else:
            print(f"❌ Log upload returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing log upload: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Auto DevOps Assistant API...")
    print("=" * 50)
    
    print("\n1. Testing basic Flask endpoint...")
    test_flask_app()
    
    print("\n2. Testing health check...")
    test_health_endpoint()
    
    print("\n3. Testing log upload...")
    test_log_upload()
    
    print("\n" + "=" * 50)
    print("🎯 Test completed!")
    print("\nTo run the Flask app manually:")
    print("python app.py")
    print("\nThen visit: http://127.0.0.1:5000")
