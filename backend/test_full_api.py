"""
Comprehensive test script for Auto DevOps Assistant API with mock database
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_basic_endpoint():
    """Test basic Flask endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Basic endpoint working!")
            print(f"   Response: {response.text}")
            return True
        else:
            print(f"❌ Basic endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing basic endpoint: {e}")
        return False

def test_health_endpoint():
    """Test health check endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print("✅ Health endpoint working!")
            print(f"   Status: {data.get('status')}")
            print(f"   Database: {data.get('database')}")
            if 'stats' in data:
                print(f"   Stats: {data['stats']}")
            return True
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing health endpoint: {e}")
        return False

def test_log_upload():
    """Test log upload with various log types"""
    test_logs = [
        {
            "content": "ERROR: yaml.scanner.ScannerError: mapping values are not allowed here\n  in \"docker-compose.yml\", line 5, column 13",
            "source": "docker",
            "description": "YAML syntax error"
        },
        {
            "content": "ERROR: docker: Error response from daemon: driver failed programming external connectivity on endpoint",
            "source": "docker", 
            "description": "Docker port conflict"
        },
        {
            "content": "kubectl error: error validating \"deployment.yaml\": ValidationError",
            "source": "kubernetes",
            "description": "Kubernetes validation error"
        }
    ]
    
    success_count = 0
    
    for i, log_data in enumerate(test_logs, 1):
        try:
            response = requests.post(
                f"{BASE_URL}/api/upload-log",
                json={
                    "log_content": log_data["content"],
                    "source": log_data["source"]
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Log upload {i} successful ({log_data['description']})")
                print(f"   Log ID: {data.get('log_id')}")
                print(f"   Severity: {data.get('analysis', {}).get('severity')}")
                print(f"   Errors found: {data.get('analysis', {}).get('errors_found')}")
                success_count += 1
            else:
                print(f"❌ Log upload {i} failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error testing log upload {i}: {e}")
    
    return success_count

def test_get_logs():
    """Test getting all logs"""
    try:
        response = requests.get(f"{BASE_URL}/api/logs")
        if response.status_code == 200:
            data = response.json()
            print("✅ Get logs endpoint working!")
            print(f"   Total logs: {data.get('count')}")
            print(f"   Database: {data.get('database')}")
            return True
        else:
            print(f"❌ Get logs failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing get logs: {e}")
        return False

def test_get_fixes():
    """Test getting fix suggestions"""
    try:
        response = requests.get(f"{BASE_URL}/api/fixes")
        if response.status_code == 200:
            data = response.json()
            print("✅ Get fixes endpoint working!")
            print(f"   Available fixes: {data.get('count')}")
            print(f"   Database: {data.get('database')}")
            if data.get('fixes'):
                print("   Sample fixes:")
                for fix in data['fixes'][:2]:  # Show first 2 fixes
                    print(f"     - {fix.get('error_type')}: {fix.get('fix_suggestion')[:50]}...")
            return True
        else:
            print(f"❌ Get fixes failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing get fixes: {e}")
        return False

def run_all_tests():
    """Run all API tests"""
    print("🧪 Auto DevOps Assistant API Test Suite")
    print("=" * 60)
    
    tests = [
        ("Basic Endpoint", test_basic_endpoint),
        ("Health Check", test_health_endpoint), 
        ("Log Upload", test_log_upload),
        ("Get Logs", test_get_logs),
        ("Get Fixes", test_get_fixes)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\\n🔍 Testing: {test_name}")
        print("-" * 40)
        result = test_func()
        results.append((test_name, result))
        
    print("\\n" + "=" * 60)
    print("📊 Test Results Summary:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\\nOverall: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All tests passed! Your Auto DevOps Assistant API is working!")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    print("Make sure Flask app is running: python app.py")
    print("Then press Enter to start testing...")
    input()
    run_all_tests()
