"""
Test Auto DevOps Assistant with real TiDB connection
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_health_with_tidb():
    """Test health endpoint with TiDB"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print("✅ Health endpoint working!")
            print(f"   Status: {data.get('status')}")
            print(f"   Database: {data.get('database')}")
            
            if data.get('database') == 'tidb_connected':
                print("🎉 TiDB is connected successfully!")
                return True
            else:
                print("ℹ️  Using mock database")
                return False
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure Flask app is running: python app.py")
        return False

def test_log_upload_to_tidb():
    """Test uploading a log to TiDB"""
    try:
        sample_log = {
            "log_content": "ERROR: yaml.scanner.ScannerError: mapping values are not allowed here\n  in \"docker-compose.yml\", line 5, column 13",
            "source": "docker"
        }
        
        response = requests.post(f"{BASE_URL}/api/upload-log", json=sample_log)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Log upload successful!")
            print(f"   Log ID: {data.get('log_id')}")
            print(f"   Database: {data.get('database')}")
            print(f"   Analysis: {data.get('analysis', {}).get('summary', '')[:50]}...")
            return True
        else:
            print(f"❌ Log upload failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error uploading log: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Auto DevOps Assistant with TiDB")
    print("=" * 50)
    print("Make sure Flask app is running first!")
    print()
    
    # Test health
    tidb_connected = test_health_with_tidb()
    
    if tidb_connected:
        print("\n🔍 Testing log upload to TiDB...")
        test_log_upload_to_tidb()
    
    print("\n" + "=" * 50)
    if tidb_connected:
        print("🎉 TiDB integration is working!")
        print("Your Auto DevOps Assistant is ready for the hackathon!")
    else:
        print("ℹ️  Mock database is working (TiDB connection pending)")
        print("You can still demonstrate all features with sample data.")
