"""
Online AI Service for Auto DevOps Assistant
Supports multiple free online AI APIs: Groq, Hugging Face, Together AI, etc.
"""

import requests
import json
import os
from typing import Dict, List, Any, Optional


class OnlineAIService:
    """Online AI service with multiple free API support"""
    
    def __init__(self):
        self.available_backends = []
        self.active_backend = None
        self.api_keys = self._load_api_keys()
        self._detect_available_backends()
    
    def _load_api_keys(self) -> Dict[str, str]:
        """Load API keys from environment variables or config"""
        return {
            "groq": os.getenv("GROQ_API_KEY", ""),
            "huggingface": os.getenv("HUGGINGFACE_API_KEY", ""),
            "together": os.getenv("TOGETHER_API_KEY", ""),
            "cohere": os.getenv("COHERE_API_KEY", "")
        }
    
    def _detect_available_backends(self):
        """Detect which online AI backends are available"""
        self.available_backends = []
        
        # Check for Groq (primary choice - super fast!)
        if self._check_groq():
            self.available_backends.append("groq")
            self.active_backend = "groq"
        
        # Check for Hugging Face Inference API
        if self._check_huggingface():
            self.available_backends.append("huggingface")
            if not self.active_backend:
                self.active_backend = "huggingface"
        
        # Check for Together AI
        if self._check_together():
            self.available_backends.append("together")
            if not self.active_backend:
                self.active_backend = "together"
        
        # Check for Cohere
        if self._check_cohere():
            self.available_backends.append("cohere")
            if not self.active_backend:
                self.active_backend = "cohere"
        
        # If no API keys, still offer free tier options
        if not self.available_backends:
            self.available_backends.append("huggingface_free")
            self.active_backend = "huggingface_free"
    
    def _check_groq(self) -> bool:
        """Check if Groq API is available"""
        api_key = self.api_keys.get("groq", "")
        if not api_key:
            print("ℹ️  Groq API key not configured")
            return False
        
        try:
            # Test Groq API with a simple request
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama3-8b-8192",
                    "messages": [{"role": "user", "content": "test"}],
                    "max_tokens": 5
                },
                timeout=10
            )
            
            if response.status_code == 200:
                print("✅ Groq API connected successfully - Lightning fast AI!")
                return True
            else:
                print(f"⚠️  Groq API test failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Groq API error: {e}")
            return False
    
    def _check_huggingface(self) -> bool:
        """Check if Hugging Face API is available"""
        api_key = self.api_keys.get("huggingface", "")
        if api_key:
            print("✅ Hugging Face API key configured")
            return True
        else:
            print("ℹ️  Hugging Face API key not configured - using free tier")
            return True  # HF has free tier without API key
    
    def _check_together(self) -> bool:
        """Check if Together AI is available"""
        api_key = self.api_keys.get("together", "")
        if api_key:
            print("✅ Together AI API key configured")
            return True
        else:
            print("ℹ️  Together AI API key not configured")
            return False
    
    def _check_cohere(self) -> bool:
        """Check if Cohere API is available"""
        api_key = self.api_keys.get("cohere", "")
        if api_key:
            print("✅ Cohere API key configured")
            return True
        else:
            print("ℹ️  Cohere API key not configured")
            return False
    
    def analyze_log(self, log_content: str, context: str = "") -> Dict[str, Any]:
        """Analyze log using the best available online AI backend"""
        
        if self.active_backend == "groq":
            return self._analyze_with_groq(log_content, context)
        elif self.active_backend == "huggingface":
            return self._analyze_with_huggingface(log_content, context)
        elif self.active_backend == "together":
            return self._analyze_with_together(log_content, context)
        elif self.active_backend == "cohere":
            return self._analyze_with_cohere(log_content, context)
        elif self.active_backend == "huggingface_free":
            return self._analyze_with_huggingface_free(log_content, context)
        else:
            return self._fallback_analysis(log_content)
    
    def _analyze_with_groq(self, log_content: str, context: str) -> Dict[str, Any]:
        """Analyze using Groq (Lightning Fast!)"""
        try:
            print("⚡ Analyzing with Groq - Lightning Speed!")
            
            api_key = self.api_keys["groq"]
            prompt = self._create_analysis_prompt(log_content, context)
            
            # Use Llama 3.1 8B for best balance of speed and quality
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama3-8b-8192",  # Fast model with 8k context
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are an expert DevOps engineer specializing in log analysis. Provide structured, actionable insights."
                        },
                        {
                            "role": "user", 
                            "content": prompt
                        }
                    ],
                    "max_tokens": 1000,
                    "temperature": 0.1,
                    "top_p": 0.9
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result["choices"][0]["message"]["content"]
                print("✅ Groq analysis complete!")
                
                return self._parse_ai_analysis(ai_response, "groq")
            else:
                print(f"❌ Groq API error: {response.status_code}")
                return self._fallback_analysis(log_content)
                
        except Exception as e:
            print(f"Groq analysis failed: {e}")
            return self._fallback_analysis(log_content)
    
    def _analyze_with_huggingface(self, log_content: str, context: str) -> Dict[str, Any]:
        """Analyze using Hugging Face Inference API"""
        try:
            print("🤗 Analyzing with Hugging Face...")
            
            api_key = self.api_keys["huggingface"]
            
            # Use a good free model for text generation
            response = requests.post(
                "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large",
                headers={"Authorization": f"Bearer {api_key}"},
                json={
                    "inputs": self._create_analysis_prompt(log_content, context)[:1000]
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    ai_response = result[0].get("generated_text", "")
                    return self._parse_ai_analysis(ai_response, "huggingface")
                else:
                    return self._fallback_analysis(log_content)
            else:
                return self._fallback_analysis(log_content)
                
        except Exception as e:
            print(f"Hugging Face analysis failed: {e}")
            return self._fallback_analysis(log_content)
    
    def _analyze_with_huggingface_free(self, log_content: str, context: str) -> Dict[str, Any]:
        """Analyze using Hugging Face free tier (no API key needed)"""
        try:
            print("🆓 Using Hugging Face free tier...")
            
            # Use a lightweight model that works without API key
            response = requests.post(
                "https://api-inference.huggingface.co/models/distilbert-base-uncased",
                json={
                    "inputs": log_content[:500]  # Limited for free tier
                },
                timeout=15
            )
            
            if response.status_code == 200:
                # For free tier, provide enhanced pattern analysis
                return self._enhanced_pattern_analysis(log_content, "huggingface_free")
            else:
                return self._fallback_analysis(log_content)
                
        except Exception as e:
            print(f"Hugging Face free analysis failed: {e}")
            return self._fallback_analysis(log_content)
    
    def _analyze_with_together(self, log_content: str, context: str) -> Dict[str, Any]:
        """Analyze using Together AI"""
        try:
            print("🤝 Analyzing with Together AI...")
            
            api_key = self.api_keys["together"]
            
            response = requests.post(
                "https://api.together.xyz/inference",
                headers={"Authorization": f"Bearer {api_key}"},
                json={
                    "model": "togethercomputer/llama-2-7b-chat",
                    "prompt": self._create_analysis_prompt(log_content, context),
                    "max_tokens": 800,
                    "temperature": 0.1
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result.get("output", {}).get("choices", [{}])[0].get("text", "")
                return self._parse_ai_analysis(ai_response, "together")
            else:
                return self._fallback_analysis(log_content)
                
        except Exception as e:
            print(f"Together AI analysis failed: {e}")
            return self._fallback_analysis(log_content)
    
    def _analyze_with_cohere(self, log_content: str, context: str) -> Dict[str, Any]:
        """Analyze using Cohere"""
        try:
            print("🔮 Analyzing with Cohere...")
            
            api_key = self.api_keys["cohere"]
            
            response = requests.post(
                "https://api.cohere.ai/v1/generate",
                headers={"Authorization": f"Bearer {api_key}"},
                json={
                    "model": "command",
                    "prompt": self._create_analysis_prompt(log_content, context),
                    "max_tokens": 800,
                    "temperature": 0.1
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result.get("generations", [{}])[0].get("text", "")
                return self._parse_ai_analysis(ai_response, "cohere")
            else:
                return self._fallback_analysis(log_content)
                
        except Exception as e:
            print(f"Cohere analysis failed: {e}")
            return self._fallback_analysis(log_content)
    
    def _create_analysis_prompt(self, log_content: str, context: str) -> str:
        """Create a structured prompt for AI analysis"""
        return f"""
Analyze the following DevOps log for issues, errors, and problems:

Context: {context}

Log Content:
{log_content[:3000]}

Please provide:
1. ISSUES FOUND: List specific issues with severity (critical, high, medium, low)
2. ROOT CAUSES: Explain likely causes for each issue
3. RECOMMENDATIONS: Provide specific actionable solutions
4. PRIORITY: Order fixes by urgency

Format your response clearly with sections.
"""
    
    def _parse_ai_analysis(self, ai_response: str, backend: str) -> Dict[str, Any]:
        """Parse AI response into structured format"""
        
        # Extract issues and recommendations from AI response
        issues = []
        recommendations = []
        
        lines = ai_response.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Detect sections more flexibly
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in ['issues found', 'problems', 'errors', '**issues**']):
                current_section = "issues"
                continue
            elif any(keyword in line_lower for keyword in ['recommendations', 'solutions', 'fixes', '**recommendations**', 'solution 1', 'solution 2']):
                current_section = "recommendations"
                continue
            elif line_lower.startswith('**root causes**'):
                current_section = "causes"
                continue
            
            # Extract content based on section
            if current_section == "issues":
                if (line.startswith('-') or line.startswith('•') or 
                    line.startswith('*') or line[0].isdigit() or 
                    line.startswith('\t*')):
                    severity = self._determine_severity(line)
                    issues.append({
                        "description": self._clean_text(line),
                        "severity": severity,
                        "type": "ai_detected", 
                        "backend": backend
                    })
            elif current_section == "recommendations":
                if (line.startswith('-') or line.startswith('•') or 
                    line.startswith('*') or line[0].isdigit() or 
                    line.startswith('\t*') or 'solution' in line_lower):
                    clean_rec = self._clean_text(line)
                    if len(clean_rec) > 10:  # Only meaningful recommendations
                        recommendations.append(clean_rec)
        
        # If no structured sections found, extract from full response
        if not recommendations and 'increase' in ai_response.lower():
            # Look for actionable advice in the response
            for line in lines:
                line = line.strip()
                if any(action in line.lower() for action in 
                      ['increase', 'add', 'upgrade', 'configure', 'implement', 'monitor', 'check', 'review']):
                    if len(line) > 20:
                        recommendations.append(self._clean_text(line))
        
        return {
            "backend": backend,
            "issues": issues,
            "recommendations": recommendations[:8],
            "summary": f"Online AI analysis using {backend} - detected {len(issues)} issues",
            "confidence": 0.9,
            "raw_response": ai_response
        }
    
    def _determine_severity(self, text: str) -> str:
        """Determine severity from text content"""
        text_lower = text.lower()
        if any(word in text_lower for word in ['critical', 'fatal', 'severe', 'emergency']):
            return "critical"
        elif any(word in text_lower for word in ['high', 'major', 'important']):
            return "high"
        elif any(word in text_lower for word in ['medium', 'moderate']):
            return "medium"
        else:
            return "low"
    
    def _clean_text(self, text: str) -> str:
        """Clean and format text for display"""
        # Remove markdown formatting and bullet points
        text = text.strip()
        text = text.lstrip('-•*\t0123456789. ')
        text = text.replace('**', '').replace('*', '')
        return text.strip()
    
    def _enhanced_pattern_analysis(self, log_content: str, backend: str) -> Dict[str, Any]:
        """Enhanced pattern analysis for free tiers"""
        # Import the pattern analysis from local AI service
        import re
        
        patterns = {
            "critical_errors": [
                r"(fatal|critical|emergency).*error",
                r"system.*crash", r"out of memory", r"disk.*full"
            ],
            "configuration_issues": [
                r"yaml.*error", r"config.*invalid", r"permission.*denied"
            ],
            "network_problems": [
                r"timeout", r"connection.*failed", r"ssl.*error"
            ]
        }
        
        issues = []
        for category, pattern_list in patterns.items():
            for pattern in pattern_list:
                matches = re.finditer(pattern, log_content, re.IGNORECASE)
                for match in matches:
                    issues.append({
                        "type": category,
                        "description": match.group(0),
                        "severity": "high" if "critical" in category else "medium",
                        "backend": backend
                    })
        
        return {
            "backend": backend,
            "issues": issues,
            "recommendations": [
                "🔍 Review critical error patterns",
                "⚙️ Validate configuration files",
                "🌐 Check network connectivity"
            ],
            "summary": f"Enhanced pattern analysis via {backend} - {len(issues)} issues found",
            "confidence": 0.8
        }
    
    def _fallback_analysis(self, log_content: str) -> Dict[str, Any]:
        """Fallback analysis when all online services fail"""
        return {
            "backend": "fallback",
            "issues": [],
            "recommendations": ["📋 Online AI services unavailable - check API keys"],
            "summary": "Fallback analysis - online AI services not available",
            "confidence": 0.5
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Get status of online AI service"""
        return {
            "available_backends": self.available_backends,
            "active_backend": self.active_backend,
            "online_ai_enabled": len(self.available_backends) > 0,
            "api_keys_configured": {
                "groq": bool(self.api_keys.get("groq")),
                "huggingface": bool(self.api_keys.get("huggingface")),
                "together": bool(self.api_keys.get("together")),
                "cohere": bool(self.api_keys.get("cohere"))
            },
            "setup_instructions": self._get_setup_instructions()
        }
    
    def _get_setup_instructions(self) -> Dict[str, str]:
        """Get setup instructions for various online AI services"""
        return {
            "groq": "1. Sign up at https://console.groq.com/ 2. Get free API key 3. Set GROQ_API_KEY environment variable",
            "huggingface": "1. Sign up at https://huggingface.co/ 2. Get API token 3. Set HUGGINGFACE_API_KEY environment variable",
            "together": "1. Sign up at https://together.ai/ 2. Get $25 free credits 3. Set TOGETHER_API_KEY environment variable",
            "cohere": "1. Sign up at https://cohere.ai/ 2. Get free API key 3. Set COHERE_API_KEY environment variable"
        }
    
    def set_api_key(self, service: str, api_key: str) -> bool:
        """Set API key for a specific service"""
        if service in self.api_keys:
            self.api_keys[service] = api_key
            # Re-detect backends with new API key
            self._detect_available_backends()
            return True
        return False
