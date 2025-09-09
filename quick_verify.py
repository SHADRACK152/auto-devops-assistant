#!/usr/bin/env python3
"""
Quick System Verification
Tests the essential components without complex dependencies
"""

import requests
import json

def test_live_system():
    """Test the live Flask system"""
    
    print("🧪 TESTING LIVE SYSTEM")
    print("=" * 40)
    
    # Test with a realistic Docker error
    test_data = {
        "log_content": "ERROR: docker: Error response from daemon\ndriver failed programming external connectivity on endpoint webapp_web_1\nBind for 0.0.0.0:80 failed: port is already allocated",
        "source": "docker",
        "enable_ai": True
    }
    
    try:
        print("📡 Making API request to Flask server...")
        response = requests.post(
            "http://localhost:5000/api/analyze-ai",
            json=test_data,
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            analysis = result.get('analysis', {})
            
            print("✅ API Response received!")
            print("=" * 40)
            
            # Check essential components
            backend = analysis.get('backend', 'unknown')
            print(f"🔧 Backend: {backend}")
            
            ai_powered = result.get('ai_powered', False) 
            print(f"🤖 AI Powered: {ai_powered}")
            
            analysis_type = analysis.get('analysis_type', 'unknown')
            print(f"📊 Analysis Type: {analysis_type}")
            
            confidence = result.get('confidence', 0)
            print(f"🎯 Confidence: {confidence}")
            
            # Check recommendations
            recommendations = analysis.get('recommendations', [])
            print(f"💡 Solutions: {len(recommendations)}")
            
            if recommendations:
                first_rec = recommendations[0]
                
                # Check for implementation code
                if 'code' in first_rec and len(first_rec['code']) > 50:
                    print("✅ Implementation code: INCLUDED")
                else:
                    print("⚠️ Implementation code: LIMITED")
                
                # Check for detailed steps
                if 'steps' in first_rec and len(first_rec['steps']) >= 3:
                    print("✅ Step-by-step guidance: INCLUDED")
                    print(f"   Example: {first_rec['steps'][0][:60]}...")
                else:
                    print("⚠️ Step-by-step guidance: LIMITED")
                
                # Check for explanations
                if 'detailed_explanation' in first_rec and len(first_rec['detailed_explanation']) > 50:
                    print("✅ Detailed explanations: INCLUDED")
                else:
                    print("⚠️ Detailed explanations: LIMITED")
            
            # Overall assessment
            print("\n" + "=" * 40)
            print("🎯 ASSESSMENT:")
            
            success_count = 0
            
            if 'groq' in backend.lower():
                print("✅ Using Groq AI (PERFECT)")
                success_count += 3
            elif 'enhanced' in backend.lower():
                print("✅ Using Enhanced Patterns (GOOD)")
                success_count += 2
            else:
                print("⚠️ Using basic patterns")
                success_count += 1
            
            if ai_powered:
                print("✅ AI-powered analysis active")
                success_count += 1
            
            if recommendations and len(recommendations[0].get('code', '')) > 50:
                print("✅ Implementation codes included")
                success_count += 1
            
            if recommendations and len(recommendations[0].get('steps', [])) >= 3:
                print("✅ Step-by-step guidance provided")
                success_count += 1
            
            if confidence > 0.8:
                print("✅ High confidence results")
                success_count += 1
            
            print(f"\n🏆 Success Score: {success_count}/7")
            
            if success_count >= 6:
                print("🎉 EXCELLENT! System working perfectly")
                print("✅ Your 'well explained solutions' request is FULFILLED!")
            elif success_count >= 4:
                print("✅ GOOD! Major improvements achieved")
                print("📈 Significant progress from basic patterns")
            else:
                print("⚠️ Some improvements needed")
            
            return success_count >= 4
            
        else:
            print(f"❌ API Error: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Flask server")
        print("💡 Make sure Flask server is running on port 5000")
        return False
        
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False


if __name__ == "__main__":
    print("🚀 VERIFYING COMPLETE SYSTEM")
    print("Testing: AI Analysis + Implementation Codes + Explanations")
    
    success = test_live_system()
    
    if success:
        print("\n🎉 SUCCESS! The system improvements are working!")
    else:
        print("\n⚠️ System needs attention or Flask server is not running")
