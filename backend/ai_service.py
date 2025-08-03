#!/usr/bin/env python3
"""
Simplified AI service that prioritizes online AI (Groq)
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Any
from dotenv import load_dotenv

# Load environment first
load_dotenv()

from online_ai_service import OnlineAIService

class SimplifiedAIAnalyzer:
    """Simplified AI analyzer focusing on online AI"""
    
    def __init__(self):
        self.online_ai = OnlineAIService()
        self.openai_available = False  # Keep for compatibility
        
    def analyze_log(self, log_content: str, source: str = "unknown") -> Dict[str, Any]:
        """Analyze log using BOTH online AI AND pattern recognition"""
        analysis_start = datetime.now()
        
        # Step 1: Always run pattern analysis for baseline
        print("🔍 Running pattern recognition analysis...")
        pattern_issues = self._basic_pattern_analysis(log_content)
        pattern_recommendations = self._generate_smart_recommendations(pattern_issues, source)
        
        # Step 2: Try online AI (Groq) for enhanced analysis
        ai_issues = []
        ai_recommendations = []
        ai_backend = "patterns"
        online_analysis = {}
        
        if self.online_ai.available_backends:
            try:
                print(f"🚀 Using {self.online_ai.active_backend} for AI analysis")
                online_analysis = self.online_ai.analyze_log(log_content, source)
                ai_issues = online_analysis.get("issues", [])
                ai_recommendations = online_analysis.get("recommendations", [])
                ai_backend = online_analysis.get("backend", "online_ai")
                print(f"✅ {ai_backend} analysis complete!")
            except Exception as e:
                print(f"❌ Online AI failed: {e}")
                online_analysis = {}
        
        # Step 3: Combine both analyses
        combined_issues = self._merge_issues(pattern_issues, ai_issues)
        combined_recommendations = self._merge_recommendations(pattern_recommendations, ai_recommendations)
        
        # Format result with combined analysis
        result = {
            "log_id": str(hash(log_content))[:8],
            "issues": combined_issues,
            "errors": combined_issues,  # Compatibility field
            "errors_found": len(combined_issues),
            "recommendations": self._format_recommendations(combined_recommendations, "Combined"),
            "analysis_type": f"Combined AI + Pattern Analysis" if ai_backend != "patterns" else "Enhanced Pattern Analysis",
            "backend": f"{ai_backend}+patterns" if ai_backend != "patterns" else "patterns",
            "confidence": 0.95 if ai_backend != "patterns" else 0.75,
            "confidence_score": 0.95 if ai_backend != "patterns" else 0.75,
            "summary": f"Combined analysis: {len(ai_issues)} AI issues + {len(pattern_issues)} pattern issues = {len(combined_issues)} total",
            "processing_time": (datetime.now() - analysis_start).total_seconds(),
            "source": source,
            "timestamp": datetime.now().isoformat(),
            "severity": self._calculate_severity(combined_issues),
            "ai_powered": ai_backend != "patterns",
            "ai_insights": online_analysis.get("raw_response", "") if ai_backend != "patterns" else "",
            "pattern_analysis": {
                "issues_found": len(pattern_issues),
                "recommendations": len(pattern_recommendations),
                "patterns_matched": self._get_matched_patterns(log_content)
            }
        }
        
        print(f"✅ Combined analysis: {len(combined_issues)} total issues, {len(combined_recommendations)} recommendations")
        return result
    
    def _basic_pattern_analysis(self, log_content: str) -> List[Dict]:
        """Enhanced pattern analysis with smart error detection"""
        issues = []
        lines = log_content.split('\n')
        
        # Smart patterns that detect specific problems, not just keywords
        smart_patterns = [
            # Database issues
            {
                'pattern': ['database', 'timeout'],
                'title': 'Database Connection Timeout',
                'severity': 'critical',
                'type': 'database',
                'description': 'Database connection timeout detected'
            },
            {
                'pattern': ['database', 'connection', 'refused'],
                'title': 'Database Connection Refused',
                'severity': 'critical',
                'type': 'database',
                'description': 'Database refusing connections'
            },
            {
                'pattern': ['database', 'connect', 'failed'],
                'title': 'Database Connection Failed',
                'severity': 'critical',
                'type': 'database',
                'description': 'Failed to establish database connection'
            },
            # Environment variable issues
            {
                'pattern': ['env', 'not set'],
                'title': 'Missing Environment Variable',
                'severity': 'high',
                'type': 'environment',
                'description': 'Required environment variable not configured'
            },
            {
                'pattern': ['database_url', 'not set'],
                'title': 'Missing DATABASE_URL',
                'severity': 'critical',
                'type': 'environment',
                'description': 'DATABASE_URL environment variable not set'
            },
            # Resource issues
            {
                'pattern': ['insufficient memory'],
                'title': 'Memory Insufficient',
                'severity': 'high',
                'type': 'resource',
                'description': 'Not enough memory available'
            },
            {
                'pattern': ['node pressure eviction'],
                'title': 'Node Under Pressure',
                'severity': 'critical',
                'type': 'resource',
                'description': 'Node evicting pods due to resource pressure'
            },
            # Deployment issues
            {
                'pattern': ['failed to create pod'],
                'title': 'Pod Creation Failed',
                'severity': 'high',
                'type': 'deployment',
                'description': 'Unable to create pods'
            },
            {
                'pattern': ['no nodes available'],
                'title': 'No Available Nodes',
                'severity': 'high',
                'type': 'scheduling',
                'description': 'No nodes available for scheduling'
            }
        ]
        
        for line in lines:
            line_lower = line.lower().strip()
            if not line_lower or '[info]' in line_lower:
                continue
                
            # Check smart patterns
            pattern_matched = False
            for pattern_config in smart_patterns:
                patterns = pattern_config['pattern']
                if all(p in line_lower for p in patterns):
                    issues.append({
                        "title": pattern_config['title'],
                        "description": pattern_config['description'],
                        "severity": pattern_config['severity'],
                        "type": pattern_config['type'],
                        "line": line.strip(),
                        "location": f"Line: {line.strip()}"
                    })
                    pattern_matched = True
                    break  # Only match first pattern per line
            
            # Fallback: Generic error detection
            if not pattern_matched and any(keyword in line_lower for keyword in ['[error]', '[critical]', 'error:', 'failed:']):
                if 'error' not in [issue['type'] for issue in issues]:  # Avoid duplicates
                    issues.append({
                        "title": "General Error Detected",
                        "description": "Error found in deployment logs",
                        "severity": "medium",
                        "type": "error",
                        "line": line.strip(),
                        "location": f"Line: {line.strip()}"
                    })
        
        return issues
    
    def _generate_basic_recommendations(self, issues: List[Dict]) -> List[str]:
        """Generate basic recommendations"""
        if not issues:
            return ["No issues detected"]
            
        recommendations = [
            "Review system resources and scaling",
            "Check Kubernetes cluster health",
            "Monitor application logs for patterns",
            "Consider implementing monitoring and alerting"
        ]
        
        return recommendations[:len(issues)]
    
    def _generate_smart_recommendations(self, issues: List[Dict], source: str) -> List[str]:
        """Generate intelligent pattern-based recommendations"""
        if not issues:
            return ["No issues detected - system appears healthy"]
        
        recommendations = []
        issue_types = [issue.get('pattern', '').lower() for issue in issues]
        
        # Kubernetes-specific recommendations
        if source.lower() == 'kubernetes' or any('kube' in str(issue) for issue in issues):
            if any('memory' in t for t in issue_types):
                recommendations.extend([
                    "Scale up node memory resources or add more nodes",
                    "Review and optimize pod memory requests and limits",
                    "Implement horizontal pod autoscaling for memory-intensive workloads"
                ])
            if any('eviction' in t for t in issue_types):
                recommendations.extend([
                    "Configure resource quotas to prevent node pressure",
                    "Monitor node capacity and implement cluster autoscaling",
                    "Review pod priority and preemption policies"
                ])
            if any('scheduling' in t for t in issue_types):
                recommendations.extend([
                    "Add more worker nodes to increase scheduling capacity",
                    "Configure node affinity and anti-affinity rules",
                    "Review resource requirements and node taints"
                ])
        
        # General recommendations based on severity
        if any(issue.get('severity') == 'critical' for issue in issues):
            recommendations.append("Immediate attention required - escalate to ops team")
        
        if any(issue.get('severity') == 'high' for issue in issues):
            recommendations.append("High priority fixes needed within 1 hour")
        
        # Add monitoring recommendations
        recommendations.extend([
            "Implement comprehensive monitoring and alerting",
            "Set up log aggregation for better visibility",
            "Create runbooks for common failure scenarios"
        ])
        
        return recommendations[:8]  # Limit to 8 recommendations
    
    def _merge_issues(self, pattern_issues: List[Dict], ai_issues: List[Dict]) -> List[Dict]:
        """Merge pattern and AI issues, removing duplicates"""
        all_issues = []
        seen_descriptions = set()
        
        # Add AI issues first (higher priority)
        for issue in ai_issues:
            desc = issue.get('description', '').lower()
            if desc not in seen_descriptions:
                issue['source'] = 'ai'
                all_issues.append(issue)
                seen_descriptions.add(desc)
        
        # Add pattern issues that don't duplicate AI issues
        for issue in pattern_issues:
            desc = issue.get('description', '').lower()
            if desc not in seen_descriptions:
                issue['source'] = 'pattern'
                all_issues.append(issue)
                seen_descriptions.add(desc)
        
        return all_issues
    
    def _merge_recommendations(self, pattern_recs: List[str], ai_recs: List[str]) -> List[str]:
        """Merge pattern and AI recommendations"""
        combined = []
        seen = set()
        
        # Add AI recommendations first
        for rec in ai_recs:
            if rec.lower() not in seen:
                combined.append(f"[AI] {rec}")
                seen.add(rec.lower())
        
        # Add pattern recommendations
        for rec in pattern_recs:
            if rec.lower() not in seen:
                combined.append(f"[Pattern] {rec}")
                seen.add(rec.lower())
        
        return combined[:10]  # Limit total recommendations
    
    def _get_matched_patterns(self, log_content: str) -> List[str]:
        """Get list of patterns that matched in the log"""
        patterns = ['insufficient memory', 'node pressure eviction', 'no nodes available', 
                   'replica set desired count not met', 'failed to create pod']
        matched = []
        for pattern in patterns:
            if pattern in log_content.lower():
                matched.append(pattern)
        return matched
    
    def _format_recommendations(self, raw_recommendations: List, analysis_type: str = "AI") -> List[Dict]:
        """Format AI recommendations for frontend display"""
        if not raw_recommendations:
            return []
        
        formatted = []
        for i, rec in enumerate(raw_recommendations):
            if isinstance(rec, str):
                # Check if it's a problem description or actual recommendation
                if any(keyword in rec.lower() for keyword in ['recommendation:', 'solution:', 'fix:', 'increase', 'add', 'configure', 'implement', 'monitor', 'review', 'scale']):
                    # This is an actual recommendation
                    title = f"[{analysis_type}] Solution {i+1}"
                    description = rec
                    code_example = self._generate_code_example(rec)
                else:
                    # This is a problem description, provide a generic solution
                    title = f"[{analysis_type}] Issue Analysis {i+1}"
                    description = f"Problem: {rec}"
                    code_example = "# Review logs and system configuration\necho 'Analyzing issue...'"
                
                formatted.append({
                    "title": title,
                    "description": description,
                    "priority": "high",
                    "fixes": [{
                        "action": "Implement Recommendation",
                        "explanation": description,
                        "priority": "high",
                        "code": code_example
                    }]
                })
            elif isinstance(rec, dict):
                # Already formatted, use as-is
                formatted.append(rec)
        
        return formatted
    
    def _generate_code_example(self, recommendation: str) -> str:
        """Generate specific, targeted code examples for recommendations"""
        rec_lower = recommendation.lower()
        
        # Database connectivity issues
        if 'database' in rec_lower and ('connect' in rec_lower or 'timeout' in rec_lower):
            return """# Test database connectivity
kubectl get pods -l app=database
kubectl logs <database-pod-name>

# Check database service and endpoints
kubectl get svc -l app=database
kubectl get endpoints <database-service-name>

# Test connection from application pod
kubectl exec -it <app-pod-name> -- nc -zv <database-host> <database-port>

# Increase connection timeout in application
# For PostgreSQL/MySQL connection strings:
# DATABASE_URL="postgresql://user:pass@host:5432/db?connect_timeout=30"
# DATABASE_URL="mysql://user:pass@host:3306/db?timeout=30s"

# Check and restart database pod if needed
kubectl describe pod <database-pod-name>
kubectl delete pod <database-pod-name>  # Forces restart

# Scale database resources if needed
kubectl patch deployment database -p '{
  "spec": {
    "template": {
      "spec": {
        "containers": [{
          "name": "database",
          "resources": {
            "requests": {"memory": "1Gi", "cpu": "500m"},
            "limits": {"memory": "2Gi", "cpu": "1000m"}
          }
        }]
      }
    }
  }
}'"""

        # Environment variable issues
        elif 'env' in rec_lower and ('variable' in rec_lower or 'database_url' in rec_lower):
            return """# Check current environment variables
kubectl get pods <app-pod-name> -o jsonpath='{.spec.containers[0].env[*]}'
kubectl exec -it <app-pod-name> -- env | grep DATABASE

# Method 1: Add environment variable to deployment
kubectl patch deployment <app-deployment> -p '{
  "spec": {
    "template": {
      "spec": {
        "containers": [{
          "name": "<container-name>",
          "env": [{
            "name": "DATABASE_URL",
            "value": "postgresql://user:password@database:5432/mydb"
          }]
        }]
      }
    }
  }
}'

# Method 2: Create and use ConfigMap
kubectl create configmap app-config \\
  --from-literal=DATABASE_URL="postgresql://user:password@database:5432/mydb"

# Apply ConfigMap to deployment
kubectl patch deployment <app-deployment> -p '{
  "spec": {
    "template": {
      "spec": {
        "containers": [{
          "name": "<container-name>",
          "envFrom": [{
            "configMapRef": {
              "name": "app-config"
            }
          }]
        }]
      }
    }
  }
}'

# Method 3: Use Secret for sensitive data
kubectl create secret generic db-secret \\
  --from-literal=DATABASE_URL="postgresql://user:password@database:5432/mydb"

kubectl patch deployment <app-deployment> -p '{
  "spec": {
    "template": {
      "spec": {
        "containers": [{
          "name": "<container-name>",
          "envFrom": [{
            "secretRef": {
              "name": "db-secret"
            }
          }]
        }]
      }
    }
  }
}'

# Verify environment variables are set
kubectl exec -it <app-pod-name> -- env | grep DATABASE_URL"""

        # Retry mechanism implementation
        elif 'retry' in rec_lower and 'timeout' in rec_lower:
            return """# Implement retry logic in application deployment
# Add readiness and liveness probes with retry
kubectl patch deployment <app-deployment> -p '{
  "spec": {
    "template": {
      "spec": {
        "containers": [{
          "name": "<container-name>",
          "readinessProbe": {
            "httpGet": {
              "path": "/health",
              "port": 8080
            },
            "initialDelaySeconds": 10,
            "periodSeconds": 5,
            "timeoutSeconds": 10,
            "failureThreshold": 3
          },
          "livenessProbe": {
            "httpGet": {
              "path": "/health",
              "port": 8080
            },
            "initialDelaySeconds": 30,
            "periodSeconds": 10,
            "timeoutSeconds": 10,
            "failureThreshold": 5
          }
        }]
      }
    }
  }
}'

# Add restart policy for automatic recovery
kubectl patch deployment <app-deployment> -p '{
  "spec": {
    "template": {
      "spec": {
        "restartPolicy": "Always"
      }
    }
  }
}'

# Create a job that retries database connection
kubectl apply -f - <<EOF
apiVersion: batch/v1
kind: Job
metadata:
  name: db-connection-test
spec:
  backoffLimit: 5
  template:
    spec:
      containers:
      - name: db-test
        image: postgres:13
        command: ["sh", "-c"]
        args:
        - |
          for i in {1..10}; do
            if pg_isready -h database -p 5432; then
              echo "Database connection successful"
              exit 0
            fi
            echo "Attempt $i failed, retrying in 5 seconds..."
            sleep 5
          done
          exit 1
      restartPolicy: Never
EOF"""

        # Memory issues
        elif 'memory' in rec_lower and 'node' in rec_lower:
            return """# Check current memory usage
kubectl top nodes
kubectl describe nodes

# Scale node resources or add more nodes
kubectl patch deployment <deployment-name> -p '{
  "spec": {
    "template": {
      "spec": {
        "containers": [{
          "name": "<container-name>",
          "resources": {
            "requests": {"memory": "512Mi", "cpu": "250m"},
            "limits": {"memory": "1Gi", "cpu": "500m"}
          }
        }]
      }
    }
  }
}'

# Add new nodes (cloud-specific)
# AWS EKS: eksctl scale nodegroup --cluster=my-cluster --nodes=3
# GKE: gcloud container clusters resize my-cluster --num-nodes=3
# Azure AKS: az aks scale --resource-group myResourceGroup --name myCluster --node-count 3"""

        # Generic fallback with specific assessment
        else:
            problem_type = "general"
            if 'database' in rec_lower:
                problem_type = "database"
            elif 'network' in rec_lower:
                problem_type = "network"
            elif 'config' in rec_lower:
                problem_type = "configuration"
            
            return f"""# Solve {problem_type} issue: {recommendation}

# Step 1: Detailed diagnosis
kubectl get pods --all-namespaces
kubectl describe pod <affected-pod-name>
kubectl logs <affected-pod-name> --previous
kubectl get events --sort-by=.metadata.creationTimestamp

# Step 2: Apply targeted fix
{"# Check database connectivity and configuration" if problem_type == "database" else ""}
{"# Verify network policies and service configurations" if problem_type == "network" else ""}
{"# Review ConfigMaps, Secrets, and environment variables" if problem_type == "configuration" else ""}

# Step 3: Verify resolution
kubectl get pods -w
kubectl logs -f <affected-pod-name>
kubectl exec -it <pod-name> -- /bin/sh  # Interactive debugging"""
    
    def _calculate_severity(self, issues: List[Dict]) -> str:
        """Calculate overall severity based on issues"""
        if not issues:
            return "INFO"
        
        severity_weights = {"critical": 4, "high": 3, "medium": 2, "low": 1}
        total_weight = 0
        count = 0
        
        for issue in issues:
            severity = issue.get("severity", "low").lower()
            if severity in severity_weights:
                total_weight += severity_weights[severity]
                count += 1
        
        if count == 0:
            return "INFO"
        
        avg_weight = total_weight / count
        if avg_weight >= 3.5:
            return "CRITICAL"
        elif avg_weight >= 2.5:
            return "ERROR"
        elif avg_weight >= 1.5:
            return "WARNING"
        else:
            return "INFO"
    
    def get_learning_stats(self) -> Dict:
        """Compatibility method"""
        return {
            "total_analyses": 0,
            "pattern_effectiveness": 0.0,
            "user_feedback_count": 0,
            "ai_status": {
                "online_ai": len(self.online_ai.available_backends) > 0,
                "groq_available": "groq" in self.online_ai.available_backends,
                "active_backend": self.online_ai.active_backend
            }
        }
    
    def provide_feedback(self, analysis_id: str, feedback_data: Dict) -> Dict:
        """Process user feedback for learning"""
        try:
            # For now, just acknowledge the feedback
            # In a full implementation, this would store feedback in database
            learning_result = {
                "message": "🤖 Thank you for your feedback! This helps me learn and improve.",
                "analysis_id": analysis_id,
                "feedback_received": {
                    "usefulness": feedback_data.get('usefulness', 3),
                    "accuracy": feedback_data.get('accuracy', True),
                    "solution_quality": feedback_data.get('solution_quality', 3),
                    "additional_feedback": feedback_data.get('additional_feedback', '')
                },
                "learning_status": "processed",
                "improvement_areas": []
            }
            
            # Analyze feedback for improvement areas
            if feedback_data.get('usefulness', 3) < 3:
                learning_result["improvement_areas"].append("Enhance recommendation usefulness")
            
            if not feedback_data.get('accuracy', True):
                learning_result["improvement_areas"].append("Improve analysis accuracy")
                
            if feedback_data.get('solution_quality', 3) < 3:
                learning_result["improvement_areas"].append("Better solution quality")
            
            if feedback_data.get('missed_issues'):
                learning_result["improvement_areas"].append("Detect more issue types")
            
            return learning_result
            
        except Exception as e:
            return {
                "message": "Thank you for your feedback!",
                "error": str(e),
                "learning_status": "error"
            }

# Create the analyzer instance
ai_analyzer = SimplifiedAIAnalyzer()

if __name__ == "__main__":
    # Test it
    test_log = """2024-08-03T16:45:23Z [ERROR] kube-apiserver: failed to create pod: insufficient memory
2024-08-03T16:45:24Z [CRITICAL] kubelet: node pressure eviction triggered
2024-08-03T16:45:25Z [ERROR] scheduler: no nodes available for pod assignment
2024-08-03T16:45:26Z [WARNING] controller-manager: replica set desired count not met"""
    
    result = ai_analyzer.analyze_log(test_log, "kubernetes")
    print(f"\n=== TEST RESULT ===")
    print(f"Analysis Type: {result['analysis_type']}")
    print(f"Backend: {result['backend']}")
    print(f"Issues Found: {len(result['issues'])}")
    print(f"Confidence: {result['confidence']}")
