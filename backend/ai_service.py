"""
AI-Powered Log Analysis Service for Auto DevOps Assistant
Integrates with OpenAI GPT and TiDB Vector Search for intelligent log analysis
"""

import re
import json
import hashlib
from typing import Dict, List, Any
from datetime import datetime
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("⚠️  OpenAI not installed, using pattern-based analysis only")

from config import OPENAI_API_KEY
import sqlite3
import os


class LearningEngine:
    """Machine learning component for pattern discovery and improvement"""
    
    def __init__(self):
        self.db_path = "learning_data.db"
        self._init_learning_database()
    
    def _init_learning_database(self):
        """Initialize learning database for storing analysis history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables for learning data
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analysis_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                log_content TEXT,
                detected_patterns TEXT,
                user_feedback TEXT,
                confidence_score REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pattern_effectiveness (
                pattern TEXT PRIMARY KEY,
                success_count INTEGER DEFAULT 0,
                failure_count INTEGER DEFAULT 0,
                avg_confidence REAL DEFAULT 0.0
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def store_analysis(self, log_content: str, patterns: list, confidence: float):
        """Store analysis results for learning"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO analysis_history (log_content, detected_patterns, confidence_score)
            VALUES (?, ?, ?)
        ''', (log_content, str(patterns), confidence))
        
        conn.commit()
        conn.close()
    
    def update_pattern_effectiveness(self, pattern: str, success: bool):
        """Update pattern effectiveness based on user feedback"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR IGNORE INTO pattern_effectiveness (pattern) VALUES (?)
        ''', (pattern,))
        
        if success:
            cursor.execute('''
                UPDATE pattern_effectiveness 
                SET success_count = success_count + 1 
                WHERE pattern = ?
            ''', (pattern,))
        else:
            cursor.execute('''
                UPDATE pattern_effectiveness 
                SET failure_count = failure_count + 1 
                WHERE pattern = ?
            ''', (pattern,))
        
        conn.commit()
        conn.close()
    
    def get_learning_insights(self):
        """Get insights from learning data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT pattern, success_count, failure_count,
                   CASE WHEN (success_count + failure_count) > 0 
                        THEN CAST(success_count AS REAL) / (success_count + failure_count)
                        ELSE 0.0 END as effectiveness
            FROM pattern_effectiveness
            ORDER BY effectiveness DESC
        ''')
        
        patterns = cursor.fetchall()
        conn.close()
        
        return patterns


class AILogAnalyzer:
    """AI-powered log analyzer using OpenAI GPT and pattern recognition"""
    
    def __init__(self):
        self.openai_available = self._setup_openai()
        self.error_patterns = self._load_error_patterns()
        self.solution_templates = self._load_solution_templates()
        self.learning_engine = LearningEngine()  # Add learning capability
    
    def _setup_openai(self) -> bool:
        """Setup OpenAI client"""
        try:
            if OPENAI_AVAILABLE and OPENAI_API_KEY and OPENAI_API_KEY != "sk-your-openai-api-key-here":
                self.client = OpenAI(api_key=OPENAI_API_KEY)
                return True
            else:
                print("ℹ️  OpenAI API key not configured, using pattern-based analysis")
                self.client = None
                return False
        except Exception as e:
            print(f"⚠️  OpenAI setup failed: {e}")
            self.client = None
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
            },
            "network_connectivity": {
                "patterns": [
                    r"connection refused",
                    r"timeout.*connecting",
                    r"no route to host",
                    r"network.*unreachable",
                    r"dns.*resolution.*failed"
                ],
                "severity": "error",
                "category": "networking",
                "source": "network"
            },
            "dependency_missing": {
                "patterns": [
                    r"module.*not found",
                    r"no such file.*package",
                    r"import.*error",
                    r"package.*not.*installed",
                    r"command not found"
                ],
                "severity": "error",
                "category": "dependencies",
                "source": "application"
            },
            "microservices_timeout": {
                "patterns": [
                    r"timeout.*connecting",
                    r"TLS handshake timeout",
                    r"deadline exceeded",
                    r"context deadline exceeded",
                    r"connection timeout",
                    r"grpc.*deadline.*exceeded",
                    r"handshake timeout.*upstream"
                ],
                "severity": "error",
                "category": "microservices",
                "source": "application"
            },
            "service_mesh_issues": {
                "patterns": [
                    r"envoy proxy",
                    r"service mesh.*sidecar",
                    r"istio.*proxy",
                    r"circuit breaker.*opened",
                    r"proxy.*timeout",
                    r"sidecar.*connection",
                    r"failure rate: \d+%"
                ],
                "severity": "warning",
                "category": "service-mesh",
                "source": "kubernetes"
            },
            "performance_degradation": {
                "patterns": [
                    r"memory usage at \d+%",
                    r"health check.*took.*\d+\.\d+s",
                    r"connection pool.*exhausted",
                    r"active: \d+/\d+.*idle: \d+/\d+",
                    r"failure rate: \d+%",
                    r"response time.*exceeded",
                    r"pool exhausted.*active: \d+/\d+"
                ],
                "severity": "critical",
                "category": "performance",
                "source": "application"
            },
            "kubernetes_health_checks": {
                "patterns": [
                    r"readiness probe failed",
                    r"liveness probe failed",
                    r"health check.*failed",
                    r"GET /ready.*503",
                    r"GET /health.*timeout",
                    r"probe.*returned.*5\d\d",
                    r"readiness probe.*GET /ready returned 503"
                ],
                "severity": "critical",
                "category": "health-monitoring",
                "source": "kubernetes"
            }
        }
    
    def _load_solution_templates(self) -> Dict[str, Dict]:
        """Load solution templates for common errors"""
        return {
            "yaml_syntax": {
                "title": "Fix YAML Syntax Error",
                "description": "Correct YAML formatting and indentation issues",
                "solutions": [
                    {
                        "priority": "high",
                        "action": "Fix Indentation",
                        "code": """# Correct YAML indentation (use spaces, not tabs)
version: '3.8'
services:
  web:
    image: nginx:latest
    ports:
      - "80:80"
    environment:
      - NODE_ENV=production""",
                        "explanation": "Ensure consistent indentation using spaces (not tabs) and proper key-value formatting"
                    },
                    {
                        "priority": "medium",
                        "action": "Validate YAML",
                        "code": "yamllint docker-compose.yml",
                        "explanation": "Use a YAML validator to check syntax before deployment"
                    }
                ]
            },
            "docker_port_conflict": {
                "title": "Resolve Port Conflict",
                "description": "Fix port allocation conflicts between containers",
                "solutions": [
                    {
                        "priority": "high",
                        "action": "Change Port Mapping",
                        "code": """# Change to an available port
ports:
  - "8080:80"  # Use port 8080 instead of 80""",
                        "explanation": "Map to a different host port to avoid conflicts"
                    },
                    {
                        "priority": "high",
                        "action": "Stop Conflicting Container",
                        "code": "docker stop $(docker ps -q --filter \"publish=80\")",
                        "explanation": "Stop the container currently using the conflicting port"
                    },
                    {
                        "priority": "medium",
                        "action": "Check Port Usage",
                        "code": "netstat -tulpn | grep :80",
                        "explanation": "Identify which process is using the port"
                    }
                ]
            },
            "kubernetes_pod_failure": {
                "title": "Fix Kubernetes Pod Issues",
                "description": "Resolve common Kubernetes pod deployment problems",
                "solutions": [
                    {
                        "priority": "high",
                        "action": "Check Pod Status",
                        "code": "kubectl describe pod <pod-name>",
                        "explanation": "Get detailed information about pod failure reasons"
                    },
                    {
                        "priority": "high",
                        "action": "Check Image Availability",
                        "code": "kubectl get events --sort-by=.metadata.creationTimestamp",
                        "explanation": "Verify that the container image exists and is accessible"
                    },
                    {
                        "priority": "medium",
                        "action": "Fix Resource Limits",
                        "code": """resources:
  limits:
    memory: "512Mi"
    cpu: "500m"
  requests:
    memory: "256Mi"
    cpu: "250m" """,
                        "explanation": "Adjust resource limits and requests appropriately"
                    }
                ]
            },
            "permission_error": {
                "title": "Fix Permission Issues",
                "description": "Resolve file and directory permission problems",
                "solutions": [
                    {
                        "priority": "high",
                        "action": "Fix File Permissions",
                        "code": "chmod 755 /path/to/directory\nchmod 644 /path/to/file",
                        "explanation": "Set appropriate permissions for directories and files"
                    },
                    {
                        "priority": "medium",
                        "action": "Run with Proper User",
                        "code": "docker run --user $(id -u):$(id -g) your-image",
                        "explanation": "Run container with appropriate user permissions"
                    }
                ]
            },
            "resource_exhaustion": {
                "title": "Address Resource Exhaustion",
                "description": "Handle memory, disk, or CPU resource issues",
                "solutions": [
                    {
                        "priority": "critical",
                        "action": "Free Up Disk Space",
                        "code": "docker system prune -a\ndocker volume prune",
                        "explanation": "Clean up unused Docker resources to free disk space"
                    },
                    {
                        "priority": "high",
                        "action": "Increase Memory Limits",
                        "code": """services:
  app:
    deploy:
      resources:
        limits:
          memory: 2G""",
                        "explanation": "Increase memory allocation for the service"
                    }
                ]
            },
            "microservices_timeout": {
                "title": "Fix Microservices Timeout Issues",
                "description": "Resolve timeout and deadline issues in distributed systems",
                "solutions": [
                    {
                        "priority": "high",
                        "action": "Increase Timeout Values",
                        "code": """# gRPC client timeout
client_timeout = 60000  # 60 seconds
# HTTP client timeout
requests.get(url, timeout=30)""",
                        "explanation": "Increase timeout values for service calls"
                    },
                    {
                        "priority": "high",
                        "action": "Check TLS Configuration",
                        "code": "kubectl get secret tls-cert -o yaml",
                        "explanation": "Verify TLS certificates are valid and not expired"
                    }
                ]
            },
            "service_mesh_issues": {
                "title": "Fix Service Mesh Problems",
                "description": "Resolve Envoy/Istio sidecar and circuit breaker issues",
                "solutions": [
                    {
                        "priority": "high",
                        "action": "Check Envoy Configuration",
                        "code": "kubectl logs <pod-name> -c istio-proxy",
                        "explanation": "Check sidecar proxy logs for configuration issues"
                    },
                    {
                        "priority": "medium",
                        "action": "Reset Circuit Breaker",
                        "code": "kubectl patch destinationrule <rule-name> --type merge -p '{\"spec\":{\"trafficPolicy\":{\"circuitBreaker\":{\"consecutiveErrors\":5}}}}'",
                        "explanation": "Adjust circuit breaker settings"
                    }
                ]
            },
            "performance_degradation": {
                "title": "Address Performance Issues",
                "description": "Fix memory, connection pool, and performance problems",
                "solutions": [
                    {
                        "priority": "critical",
                        "action": "Scale Connection Pool",
                        "code": """# Database connection pool
max_connections: 200
min_connections: 20
connection_timeout: 30s""",
                        "explanation": "Increase database connection pool size"
                    },
                    {
                        "priority": "high",
                        "action": "Add Memory Limits",
                        "code": """resources:
  limits:
    memory: "4Gi"
    cpu: "2000m"
  requests:
    memory: "2Gi"
    cpu: "1000m" """,
                        "explanation": "Set appropriate resource limits"
                    }
                ]
            },
            "kubernetes_health_checks": {
                "title": "Fix Kubernetes Health Check Failures",
                "description": "Resolve readiness and liveness probe issues",
                "solutions": [
                    {
                        "priority": "critical",
                        "action": "Fix Health Endpoint",
                        "code": """readinessProbe:
  httpGet:
    path: /ready
    port: 8080
  initialDelaySeconds: 30
  periodSeconds: 10
  timeoutSeconds: 5""",
                        "explanation": "Configure proper health check endpoints"
                    },
                    {
                        "priority": "high",
                        "action": "Check Service Health",
                        "code": "kubectl describe pod <pod-name>\nkubectl logs <pod-name>",
                        "explanation": "Investigate why health checks are failing"
                    }
                ]
            }
        }
    
    def analyze_log(self, log_content: str, 
                   source: str = "unknown") -> Dict[str, Any]:
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
        
        # Step 5: Store learning data
        self.learning_engine.store_analysis(
            log_content, 
            [match["type"] for match in pattern_results],
            analysis["confidence_score"]
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
        analysis = {
            "detected_source": self._detect_source(log_content),
            "confidence": 0.0,
            "source_specific_issues": []
        }
        
        if source == "docker" or "docker" in log_content.lower():
            analysis.update(self._analyze_docker_log(log_content))
        elif source == "kubernetes" or any(k8s_word in log_content.lower() for k8s_word in ["kubectl", "kubernetes", "k8s", "pod"]):
            analysis.update(self._analyze_kubernetes_log(log_content))
        elif source == "yaml" or "yaml" in log_content.lower():
            analysis.update(self._analyze_yaml_log(log_content))
        
        return analysis
    
    def _detect_source(self, log_content: str) -> str:
        """Automatically detect the log source"""
        content_lower = log_content.lower()
        
        source_indicators = {
            "docker": ["docker", "container", "image", "dockerfile"],
            "kubernetes": ["kubectl", "kubernetes", "k8s", "pod", "deployment", "service"],
            "yaml": ["yaml", "yml", "scanner", "mapping"],
            "jenkins": ["jenkins", "build", "pipeline"],
            "nginx": ["nginx", "access_log", "error_log"],
            "application": ["exception", "traceback", "stack trace"]
        }
        
        scores = {}
        for source, indicators in source_indicators.items():
            scores[source] = sum(1 for indicator in indicators if indicator in content_lower)
        
        return max(scores, key=scores.get) if max(scores.values()) > 0 else "unknown"
    
    def _analyze_docker_log(self, log_content: str) -> Dict:
        """Docker-specific log analysis"""
        return {
            "docker_issues": {
                "port_conflicts": bool(re.search(r"port.*already.*allocated", log_content, re.IGNORECASE)),
                "image_issues": bool(re.search(r"pull.*image", log_content, re.IGNORECASE)),
                "build_failures": bool(re.search(r"failed.*build", log_content, re.IGNORECASE)),
                "permission_issues": bool(re.search(r"permission.*denied", log_content, re.IGNORECASE))
            }
        }
    
    def _analyze_kubernetes_log(self, log_content: str) -> Dict:
        """Kubernetes-specific log analysis"""
        return {
            "kubernetes_issues": {
                "pod_failures": bool(re.search(r"pod.*failed", log_content, re.IGNORECASE)),
                "image_pull_errors": bool(re.search(r"imagepullbackoff|errimagepull", log_content, re.IGNORECASE)),
                "resource_issues": bool(re.search(r"resource.*exceeded", log_content, re.IGNORECASE)),
                "config_errors": bool(re.search(r"configmap|secret.*not.*found", log_content, re.IGNORECASE))
            }
        }
    
    def _analyze_yaml_log(self, log_content: str) -> Dict:
        """YAML-specific log analysis"""
        return {
            "yaml_issues": {
                "syntax_errors": bool(re.search(r"yaml.*error|scanner.*error", log_content, re.IGNORECASE)),
                "indentation_errors": bool(re.search(r"mapping.*not.*allowed|indentation", log_content, re.IGNORECASE)),
                "duplicate_keys": bool(re.search(r"duplicate.*key", log_content, re.IGNORECASE))
            }
        }
    
    def _get_ai_insights(self, log_content: str) -> Dict:
        """Get AI-powered insights using OpenAI GPT"""
        try:
            if not self.client:
                return {"error": "OpenAI client not initialized", "ai_available": False}
            
            prompt = self._create_ai_prompt(log_content)
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert DevOps engineer specializing in deployment troubleshooting."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.3
            )
            
            ai_response = response.choices[0].message.content
            return self._parse_ai_response(ai_response)
            
        except Exception as e:
            print(f"AI analysis failed: {e}")
            return {"error": str(e), "ai_available": False}
    
    def _create_ai_prompt(self, log_content: str) -> str:
        """Create a structured prompt for AI analysis"""
        return f"""
        Analyze the following deployment log and provide structured insights:

        LOG CONTENT:
        {log_content[:2000]}  # Limit to avoid token limits

        Please provide:
        1. Root cause analysis
        2. Severity assessment (low/medium/high/critical)
        3. Specific fix recommendations
        4. Prevention strategies

        Format your response as JSON with keys: root_cause, severity, fixes, prevention
        """
    
    def _parse_ai_response(self, ai_response: str) -> Dict:
        """Parse AI response into structured format"""
        try:
            # Try to extract JSON from the response
            json_start = ai_response.find('{')
            json_end = ai_response.rfind('}') + 1
            
            if json_start != -1 and json_end != -1:
                json_str = ai_response[json_start:json_end]
                return json.loads(json_str)
            else:
                # Fallback: parse as plain text
                return {
                    "ai_analysis": ai_response,
                    "parsed": False
                }
        except Exception as e:
            return {
                "ai_analysis": ai_response,
                "parsing_error": str(e),
                "parsed": False
            }
    
    def _compile_analysis(self, log_content: str, pattern_results: List,
                         source_analysis: Dict, ai_insights: Dict = None) -> Dict:
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
    
    def provide_feedback(self, log_id: str, pattern_type: str, helpful: bool):
        """Allow users to provide feedback on analysis accuracy"""
        self.learning_engine.update_pattern_effectiveness(pattern_type, helpful)
        return {"status": "feedback_recorded", "log_id": log_id}
    
    def get_learning_stats(self):
        """Get learning and improvement statistics"""
        insights = self.learning_engine.get_learning_insights()
        return {
            "total_patterns": len(insights),
            "most_effective_patterns": insights[:5],
            "learning_enabled": True,
            "database_path": self.learning_engine.db_path
        }


# Create global AI analyzer instance
ai_analyzer = AILogAnalyzer()
