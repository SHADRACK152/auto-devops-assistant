import requests
import json

# Simple test to see current behavior
test_data = {
    "log_content": "2024-08-03T16:45:23Z [ERROR] test error",
    "source": "kubernetes"
}

print("🧪 QUICK TEST - Current AI Behavior")
print("=" * 40)

try:
    response = requests.post(
        "http://localhost:5000/api/analyze-ai",
        json=test_data,
        timeout=10
    )
    
    if response.status_code == 200:
        result = response.json()
        analysis = result.get('analysis', {})
        
        print(f"✅ Status: {response.status_code}")
        print(f"🔧 Backend: {analysis.get('backend', 'unknown')}")
        print(f"📊 Analysis Type: {analysis.get('analysis_type', 'unknown')}")
        print(f"🤖 AI Powered: {result.get('ai_powered', False)}")
        
        # Check what we're actually getting
        if 'groq' in analysis.get('backend', '').lower():
            print("🎉 SUCCESS: Using Groq AI!")
        elif 'enhanced' in analysis.get('backend', '').lower():
            print("✅ IMPROVED: Using Enhanced Patterns!")
        else:
            print("⚠️ Still using old fallback patterns")
            
    else:
        print(f"❌ Error: {response.status_code}")
        
except Exception as e:
    print(f"❌ Connection error: {e}")
