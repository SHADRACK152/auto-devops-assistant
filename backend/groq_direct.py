#!/usr/bin/env python3
"""
Direct Groq AI Service - Bypass Flask Integration Issues
Created: 2024-12-28
Purpose: Standalone Groq API integration to provide high-quality AI analysis
"""

import os
from groq import Groq
import json
from datetime import datetime

def analyze_with_groq_direct(log_content, source="auto-detect"):
    """
    Direct Groq AI analysis bypassing all initialization issues
    Returns comprehensive DevOps analysis with detailed explanations
    """
    try:
        # Initialize Groq client directly
        groq_api_key = os.getenv('GROQ_API_KEY')
        if not groq_api_key:
            print("❌ GROQ_API_KEY not found in environment")
            return None
            
        client = Groq(api_key=groq_api_key)
        
        # Enhanced DevOps-focused prompt for comprehensive analysis
        analysis_prompt = f"""
You are an expert DevOps engineer and system administrator analyzing logs to provide comprehensive solutions and automated recommendations.

CRITICAL REQUIREMENTS:
1. Provide ONE comprehensive solution instead of multiple repetitive options
2. Include detailed explanations for every recommendation
3. Focus on root cause analysis and prevention
4. Provide specific implementation steps
5. Include automation recommendations where applicable

LOG CONTENT TO ANALYZE:
{log_content}

SOURCE: {source}

Please provide a comprehensive analysis including:
1. **Root Cause Analysis**: Deep technical explanation of what's happening
2. **Severity Assessment**: Critical/High/Medium/Low with justification
3. **Detailed Solution**: Step-by-step implementation with explanations
4. **Prevention Strategy**: How to avoid this issue in the future
5. **Automation Opportunities**: Scripts, monitoring, or tools to implement
6. **Best Practices**: Industry-standard recommendations

Focus on providing one high-quality, well-explained solution rather than multiple generic options.
"""

        # Call Groq API with optimized parameters
        print("🚀 Calling Groq AI directly...")
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert DevOps engineer providing comprehensive, detailed solutions with thorough explanations. Always provide root cause analysis, specific implementation steps, and automation recommendations."
                },
                {
                    "role": "user", 
                    "content": analysis_prompt
                }
            ],
            max_tokens=4000,
            temperature=0.3,
            top_p=0.9
        )
        
        # Extract and process the analysis
        ai_analysis = response.choices[0].message.content
        
        # Parse the log content for basic metrics
        lines = log_content.split('\n')
        error_count = sum(1 for line in lines if any(level in line.lower() for level in ['error', 'exception', 'fail', 'critical']))
        warning_count = sum(1 for line in lines if any(level in line.lower() for level in ['warn', 'warning']))
        
        # Determine severity based on content analysis
        severity = "Low"
        if error_count > 5 or "critical" in log_content.lower() or "exception" in log_content.lower():
            severity = "High"
        elif error_count > 0 or warning_count > 3:
            severity = "Medium"
        
        # Structure the comprehensive response
        result = {
            "ai_powered": True,
            "backend": "groq_ai_direct",
            "analysis_timestamp": datetime.now().isoformat(),
            "severity": severity,
            "confidence_score": 0.95,
            "summary": f"Comprehensive AI analysis completed - {len(ai_analysis)} characters of detailed insights",
            "detailed_analysis": ai_analysis,
            "metrics": {
                "error_count": error_count,
                "warning_count": warning_count,
                "log_lines": len(lines),
                "analysis_length": len(ai_analysis)
            },
            "recommendations": ai_analysis,  # Full AI response as recommendations
            "automation_suggestions": "See detailed analysis for automation opportunities",
            "next_steps": "Follow the implementation steps provided in the detailed analysis"
        }
        
        print(f"✅ Direct Groq analysis complete: {len(ai_analysis)} characters")
        return result
        
    except Exception as e:
        print(f"❌ Direct Groq error: {str(e)}")
        return None

def test_groq_connection():
    """Test Groq API connectivity"""
    try:
        groq_api_key = os.getenv('GROQ_API_KEY')
        if not groq_api_key:
            return False, "No GROQ_API_KEY found"
            
        client = Groq(api_key=groq_api_key)
        
        # Simple test call
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": "Test connection"}],
            max_tokens=10
        )
        
        return True, "Connection successful"
        
    except Exception as e:
        return False, f"Connection failed: {str(e)}"

if __name__ == "__main__":
    # Test the direct service
    test_log = """
2024-12-28 10:30:15 ERROR Database connection failed: Connection timeout
2024-12-28 10:30:16 WARN Retrying connection attempt 1/3
2024-12-28 10:30:20 ERROR Database connection failed: Connection timeout
2024-12-28 10:30:21 WARN Retrying connection attempt 2/3
2024-12-28 10:30:25 ERROR Database connection failed: Connection timeout
2024-12-28 10:30:26 ERROR Max retry attempts reached, service unavailable
"""
    
    print("🧪 Testing direct Groq service...")
    result = analyze_with_groq_direct(test_log, "database")
    
    if result:
        print(f"✅ Test successful!")
        print(f"Analysis length: {len(result.get('detailed_analysis', ''))} characters")
        print(f"Severity: {result.get('severity')}")
    else:
        print("❌ Test failed")
