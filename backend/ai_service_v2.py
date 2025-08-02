"""
AI-Powered Log Analysis Service for Auto DevOps Assistant
Simplified version with robust pattern recognition and OpenAI integration
"""

import re
import json
import hashlib
from typing import Dict, List, Any, Optional
from datetime import datetime

# Try to import OpenAI, gracefully handle if not available
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class AILogAnalyzer:
    """AI-powered log analyzer using OpenAI GPT and pattern recognition"""
    
    def __init__(self):
        self.openai_available = False
        self.client = None
        self._setup_openai()
        self.error_patterns = self._load_error_patterns()
        self.solution_templates = self._load_solution_templates()
    
    def _setup_openai(self) -> bool:
        """Setup OpenAI client"""
        try:
            if OPENAI_AVAILABLE:
                from config import OPENAI_API_KEY
                if OPENAI_API_KEY and not OPENAI_API_KEY.startswith("sk-your-"):
                    self.client = OpenAI(api_key=OPENAI_API_KEY)
                    self.openai_available = True
                    print("✅ OpenAI client initialized successfully!")
                    return True
            
            print("ℹ️  OpenAI not available, using advanced pattern recognition")
            return False
        except Exception as e:
            print(f"⚠️  OpenAI setup failed: {e}")
            return False
    
    def _load_error_patterns(self) -> Dict[str, Dict]:
        """Load comprehensive error patterns for log analysis"""
        return {
            "yaml_syntax": {
                "patterns": [
                    r"yaml\.scanner\.ScannerError",
                    r"mapping values are not allowed here",
                    r"found character.*that cannot start any token",
                    r"expected.*but found",
                    r"could not find expected.*",
                    r"duplicate key"
                ],
                "severity": "error",
                "category": "configuration",
                "source": "yaml"
            },
            "docker_port_conflict": {
                "patterns": [
                    r"port is already allocated",
                    r"bind.*failed.*port.*already.*use",
                    r"address already in use",
                    r"port.*already.*allocated"
                ],
                "severity": "error",
                "category": "networking",
                "source": "docker"
            },
            "kubernetes_pod_failure": {
                "patterns": [
                    r"pods.*is forbidden",
                    r"ImagePullBackOff",
                    r"CrashLoopBackOff",
                    r"CreateContainerConfigError",
                    r"ErrImagePull",
                    r"pods.*not found"
                ],
                "severity": "error",
                "category": "orchestration",
                "source": "kubernetes"
            },
            "docker_build_failure": {
                "patterns": [
                    r"failed to build",
                    r"error building image",
                    r"dockerfile.*not found",
                    r"no such file or directory.*dockerfile",
                    r"step.*failed"
                ],
                "severity": "error",
                "category": "build",
                "source": "docker"
            },
            "permission_error": {
                "patterns": [
                    r"permission denied",
                    r"access denied",
                    r"forbidden",
                    r"unauthorized",
                    r"403.*forbidden"
                ],
                "severity": "error",
                "category": "security",
                "source": "system"
            },
            "resource_exhaustion": {
                "patterns": [
                    r"out of memory",
                    r"disk.*full",
                    r"no space left",
                    r"resource.*exhausted",
                    r"memory.*exceeded"
                ],
                "severity": "critical",
                "category": "resources",
                "source": "system"
            }
        }
    
    def _load_solution_templates(self) -> Dict[str, Dict]:
        """Load solution templates for common errors"""
        return {
            "yaml_syntax": {
                "title": "Fix YAML Syntax Error",
                "description": "Correct YAML formatting and indentation",
                "solutions": [
                    {
                        "priority": "high",
                        "action": "Fix Indentation",
                        "code": """version: '3.8'
services:
  web:
    image: nginx:latest
    ports:
      - "80:80"
    environment:
      - NODE_ENV=production""",
                        "explanation": "Use consistent indentation with spaces"
                    }
                ]
            },
            "docker_port_conflict": {
                "title": "Resolve Port Conflict",
                "description": "Fix port allocation conflicts",
                "solutions": [
                    {
                        "priority": "high",
                        "action": "Change Port Mapping",
                        "code": """ports:
  - "8080:80"  # Use port 8080 instead""",
                        "explanation": "Map to a different host port"
                    },
                    {
                        "priority": "high",
                        "action": "Stop Conflicting Container",
                        "code": "docker stop $(docker ps -q --filter \"publish=80\")",
                        "explanation": "Stop container using the port"
                    }
                ]
            }
        }
    
    def analyze_log(self, log_content: str, source: str = "unknown") -> Dict[str, Any]:
        """
        Comprehensive log analysis using AI and pattern recognition
        """
        analysis_start = datetime.now()
        
        # Step 1: Pattern-based analysis
        pattern_results = self._analyze_patterns(log_content)
        
        # Step 2: Source-specific analysis
        source_analysis = self._analyze_by_source(log_content, source)
        
        # Step 3: AI-powered analysis (if available)
        ai_insights = None
        if self.openai_available:
            ai_insights = self._get_ai_insights(log_content)
        
        # Step 4: Generate comprehensive analysis
        analysis = self._compile_analysis(
            log_content, pattern_results, source_analysis, ai_insights
        )
        
        analysis["analysis_time"] = (datetime.now() - analysis_start).total_seconds()
        analysis["ai_powered"] = self.openai_available
        
        return analysis
    
    def _analyze_patterns(self, log_content: str) -> List[Dict]:
        """Analyze log using predefined error patterns"""
        matches = []
        lines = log_content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            for error_type, pattern_config in self.error_patterns.items():
                for pattern in pattern_config["patterns"]:
                    if re.search(pattern, line, re.IGNORECASE):
                        matches.append({
                            "type": error_type,
                            "line_number": line_num,
                            "line_content": line.strip(),
                            "pattern": pattern,
                            "severity": pattern_config["severity"],
                            "category": pattern_config["category"],
                            "source": pattern_config["source"]
                        })
        
        return matches
    
    def _analyze_by_source(self, log_content: str, source: str) -> Dict:
        """Source-specific analysis logic"""
        return {
            "detected_source": self._detect_source(log_content),
            "confidence": 0.8,
            "source_specific_issues": []
        }
    
    def _detect_source(self, log_content: str) -> str:
        """Automatically detect the log source"""
        content_lower = log_content.lower()
        
        if "yaml" in content_lower or "scanner" in content_lower:
            return "yaml"
        elif "docker" in content_lower or "container" in content_lower:
            return "docker"
        elif any(k8s in content_lower for k8s in ["kubectl", "kubernetes", "k8s", "pod"]):
            return "kubernetes"
        elif "jenkins" in content_lower or "build" in content_lower:
            return "jenkins"
        else:
            return "application"
    
    def _get_ai_insights(self, log_content: str) -> Optional[Dict]:
        """Get AI-powered insights using OpenAI GPT"""
        try:
            if not self.client:
                return None
            
            prompt = f"""Analyze this deployment log and provide insights:

LOG:
{log_content[:1500]}

Provide a brief analysis focusing on:
1. Root cause
2. Severity (critical/error/warning/info)
3. Quick fix recommendation

Keep response under 200 words."""
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a DevOps expert."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.3
            )
            
            ai_response = response.choices[0].message.content
            return {
                "ai_analysis": ai_response,
                "ai_available": True
            }
            
        except Exception as e:
            print(f"AI analysis failed: {e}")
            return {"error": str(e), "ai_available": False}
    
    def _compile_analysis(self, log_content: str, pattern_results: List,
                         source_analysis: Dict, ai_insights: Optional[Dict] = None) -> Dict:
        """Compile comprehensive analysis results"""
        
        # Determine overall severity
        severities = [match["severity"] for match in pattern_results]
        severity_priority = {"critical": 4, "error": 3, "warning": 2, "info": 1}
        overall_severity = "info"
        
        if severities:
            max_severity = max(severities, key=lambda x: severity_priority.get(x, 0))
            overall_severity = max_severity
        
        # Generate solutions
        solutions = self._generate_solutions(pattern_results)
        
        # Create summary
        summary = self._create_summary(pattern_results, source_analysis, overall_severity)
        
        return {
            "log_id": hashlib.md5(log_content.encode()).hexdigest()[:8],
            "timestamp": datetime.now().isoformat(),
            "severity": overall_severity,
            "summary": summary,
            "detected_source": source_analysis.get("detected_source", "unknown"),
            "errors_found": len(pattern_results),
            "pattern_matches": pattern_results,
            "source_analysis": source_analysis,
            "ai_insights": ai_insights,
            "solutions": solutions,
            "categories": list(set(match["category"] for match in pattern_results)),
            "confidence_score": self._calculate_confidence(pattern_results, source_analysis)
        }
    
    def _generate_solutions(self, pattern_results: List) -> List[Dict]:
        """Generate solution recommendations based on detected patterns"""
        solutions = []
        
        # Group errors by type
        error_types = set(match["type"] for match in pattern_results)
        
        for error_type in error_types:
            if error_type in self.solution_templates:
                template = self.solution_templates[error_type]
                solutions.append({
                    "error_type": error_type,
                    "title": template["title"],
                    "description": template["description"],
                    "fixes": template["solutions"]
                })
        
        return solutions
    
    def _create_summary(self, pattern_results: List, source_analysis: Dict, severity: str) -> str:
        """Create a human-readable summary of the analysis"""
        if not pattern_results:
            return "Log analysis completed. No critical issues detected."
        
        error_count = len(pattern_results)
        categories = set(match["category"] for match in pattern_results)
        detected_source = source_analysis.get("detected_source", "unknown")
        
        summary = f"Found {error_count} issue(s) in {detected_source} deployment log. "
        summary += f"Primary categories: {', '.join(categories)}. "
        summary += f"Severity: {severity.upper()}."
        
        return summary
    
    def _calculate_confidence(self, pattern_results: List, source_analysis: Dict) -> float:
        """Calculate confidence score for the analysis"""
        base_confidence = 0.5
        
        # Increase confidence based on pattern matches
        pattern_confidence = min(len(pattern_results) * 0.1, 0.3)
        
        # Increase confidence if source is detected
        source_confidence = 0.2 if source_analysis.get("detected_source", "unknown") != "unknown" else 0
        
        return min(base_confidence + pattern_confidence + source_confidence, 1.0)


# Create global AI analyzer instance
ai_analyzer = AILogAnalyzer()
