#!/usr/bin/env python3
"""
Enhanced AI Service with TiDB Pattern Recognition
Provides single, finalized solutions instead of multiple recommendations
"""
import os
import json
from datetime import datetime
from typing import Dict, Any, List
from dotenv import load_dotenv

# Load environment first
load_dotenv()

from online_ai_service import OnlineAIService
from enhanced_pattern_recognition import enhanced_pattern_recognition

class SimplifiedAIAnalyzer:
    """Enhanced AI analyzer with single solution output"""
    
    def __init__(self):
        self.online_ai = OnlineAIService()
        self.pattern_recognition = enhanced_pattern_recognition
        self.openai_available = False  # Keep for compatibility
        print("✅ Enhanced AI Analyzer initialized with TiDB pattern recognition")
    
    def analyze_log(self, log_content: str, source: str = "unknown") -> Dict[str, Any]:
        """
        Analyze log and provide a SINGLE comprehensive solution
        No more multiple sections - one finalized solution only
        """
        analysis_start = datetime.now()
        print(f"🔍 Analyzing {len(log_content)} characters of log content...")
        
        # Try online AI first for enhanced analysis
        if self.online_ai.available_backends:
            try:
                print(f"🚀 Using {self.online_ai.active_backend} for AI analysis...")
                online_analysis = self.online_ai.analyze_log(log_content, source)
                
                if online_analysis and online_analysis.get("issues"):
                    # AI found issues - create a comprehensive solution
                    ai_solution = self._create_ai_solution(online_analysis, log_content)
                    
                    # Store this pattern for future learning
                    pattern_id = self.pattern_recognition.vector_search.store_deployment_pattern(
                        log_content, 
                        online_analysis.get("issues", []),
                        [ai_solution]
                    )
                    
                    return {
                        "analysis_type": "AI-Enhanced Single Solution",
                        "backend": f"{online_analysis.get('backend', 'ai')}+tidb",
                        "confidence": min(online_analysis.get("confidence", 0.85), 0.98),
                        "confidence_score": min(online_analysis.get("confidence", 0.85), 0.98),
                        
                        # Single comprehensive solution
                        "solution": ai_solution,
                        
                        # Summary information
                        "issues_summary": {
                            "total_issues": len(online_analysis.get("issues", [])),
                            "primary_issue": online_analysis.get("issues", [{}])[0].get("title", "Unknown Issue"),
                            "ai_powered": True
                        },
                        
                        "pattern_analysis": {
                            "ai_insights": True,
                            "stored_in_tidb": True,
                            "pattern_id": pattern_id
                        },
                        
                        "processing_time": (datetime.now() - analysis_start).total_seconds(),
                        "timestamp": datetime.now().isoformat(),
                        "source": source
                    }
                    
            except Exception as e:
                print(f"❌ AI analysis failed: {e}")
        
        # Fallback to enhanced pattern recognition
        print("🔍 Using enhanced pattern recognition with TiDB...")
        pattern_result = self.pattern_recognition.analyze_and_solve(log_content, source)
        
        return pattern_result
    
    def _create_ai_solution(self, ai_analysis: Dict, log_content: str) -> Dict[str, Any]:
        """Create a single comprehensive solution from AI analysis"""
        
        issues = ai_analysis.get("issues", [])
        recommendations = ai_analysis.get("recommendations", [])
        
        if not issues:
            return self._get_generic_ai_solution(log_content)
        
        # Determine the primary issue type
        primary_issue = issues[0]
        issue_type = primary_issue.get("type", "general").lower()
        
        # Generate solution based on primary issue
        solution_title = f"Complete {primary_issue.get('title', 'System Issue')} Resolution"
        
        # Create comprehensive steps
        solution_steps = []
        if recommendations:
            # Use AI recommendations to create structured steps
            for i, rec in enumerate(recommendations[:5], 1):
                if isinstance(rec, dict):
                    step_text = rec.get("text", rec.get("recommendation", str(rec)))
                else:
                    step_text = str(rec)
                solution_steps.append(f"{i}. {step_text}")
        else:
            # Generate steps based on issue type
            solution_steps = self._generate_steps_for_issue_type(issue_type, primary_issue)
        
        # Generate code example
        code_example = self._generate_code_for_issue_type(issue_type, primary_issue, log_content)
        
        # Estimate success rate based on issue severity and AI confidence
        base_confidence = ai_analysis.get("confidence", 0.8)
        issue_severity = primary_issue.get("severity", "medium")
        severity_multipliers = {"critical": 0.85, "high": 0.90, "medium": 0.93, "low": 0.95}
        success_rate = base_confidence * severity_multipliers.get(issue_severity, 0.90)
        
        return {
            "title": solution_title,
            "steps": solution_steps,
            "code_example": code_example,
            "estimated_time": self._estimate_time_for_issue(issue_type, len(issues)),
            "success_rate": min(success_rate, 0.98),
            "pattern_id": f"ai_{issue_type}_{hash(log_content) % 10000}",
            "ai_generated": True
        }
    
    def _generate_steps_for_issue_type(self, issue_type: str, issue: Dict) -> List[str]:
        """Generate solution steps based on issue type"""
        
        step_templates = {
            "docker": [
                "1. Verify Docker build context contains all required files",
                "2. Check .dockerignore is not excluding necessary files", 
                "3. Rebuild with --no-cache flag to ensure fresh build",
                "4. Test the resulting container functionality",
                "5. Monitor build logs for any remaining issues"
            ],
            "kubernetes": [
                "1. Check cluster health and node availability",
                "2. Verify resource quotas and limits are sufficient",
                "3. Review and update deployment configuration",
                "4. Apply fixes and monitor pod status", 
                "5. Validate application is running correctly"
            ],
            "database": [
                "1. Verify database server connectivity and status",
                "2. Check user permissions and authentication",
                "3. Run necessary migrations or schema updates",
                "4. Test application database connections",
                "5. Monitor connection stability and performance"
            ],
            "network": [
                "1. Test basic network connectivity and DNS resolution",
                "2. Check firewall rules and security group settings",
                "3. Verify service endpoints and port accessibility",
                "4. Update network configuration as needed",
                "5. Validate application network communications"
            ]
        }
        
        # Match issue type to step template
        for key in step_templates:
            if key in issue_type or key in issue.get("description", "").lower():
                return step_templates[key]
        
        # Generic steps if no specific match
        return [
            "1. Identify the root cause of the reported issue",
            "2. Review system logs and error messages thoroughly", 
            "3. Apply appropriate configuration or code fixes",
            "4. Test the solution in a safe environment",
            "5. Deploy and monitor the resolution"
        ]
    
    def _generate_code_for_issue_type(self, issue_type: str, issue: Dict, log_content: str) -> str:
        """Generate code example based on issue type"""
        
        issue_desc = issue.get("description", "").lower()
        issue_line = issue.get("line", "").lower()
        combined_text = f"{issue_type} {issue_desc} {issue_line}".lower()
        
        if "docker" in combined_text or "copy failed" in combined_text:
            return '''# COMPLETE DOCKER BUILD FIX
echo "🔧 Resolving Docker build issues..."

# Check build context
find . -name "requirements.txt" -o -name "package.json" -o -name "Dockerfile"

# Temporary disable .dockerignore
[ -f .dockerignore ] && mv .dockerignore .dockerignore.backup

# Clean rebuild
docker build --no-cache --progress=plain -t fixed-app .

# Test result
docker run --rm fixed-app echo "Build successful!"
'''
        
        elif "kubernetes" in combined_text or "pod" in combined_text:
            return '''# COMPLETE KUBERNETES FIX
echo "🔧 Resolving Kubernetes deployment issues..."

# Check cluster status
kubectl cluster-info
kubectl get nodes

# Review deployment
kubectl describe deployment $APP_NAME
kubectl get pods -l app=$APP_NAME

# Apply fixes
kubectl rollout restart deployment/$APP_NAME
kubectl rollout status deployment/$APP_NAME
'''
        
        elif "database" in combined_text or "mysql" in combined_text or "postgres" in combined_text:
            return '''# COMPLETE DATABASE FIX
echo "🔧 Resolving database connection issues..."

# Test connectivity
ping -c 3 $DB_HOST
telnet $DB_HOST $DB_PORT

# Check credentials and run migrations
python manage.py migrate 2>/dev/null || \\
npx sequelize-cli db:migrate 2>/dev/null || \\
php artisan migrate 2>/dev/null

# Verify connection
echo "SELECT 1;" | psql $DATABASE_URL || \\
echo "SELECT 1;" | mysql -h $DB_HOST -u $DB_USER -p$DB_PASSWORD $DB_NAME
'''
        
        else:
            return '''# GENERAL SYSTEM FIX
echo "🔧 Running comprehensive system resolution..."

# Health check
kubectl get all 2>/dev/null || docker ps -a
systemctl --failed

# Resource check
df -h | grep -E "(9[0-9]%|100%)"
free -h

# Log analysis
tail -100 /var/log/syslog | grep -i error
kubectl logs -l app=$APP_NAME --tail=50 2>/dev/null

echo "✅ System analysis complete"
'''
    
    def _estimate_time_for_issue(self, issue_type: str, issue_count: int) -> str:
        """Estimate resolution time based on issue type and complexity"""
        
        base_times = {
            "docker": "10-20 minutes",
            "kubernetes": "15-30 minutes", 
            "database": "20-40 minutes",
            "network": "15-25 minutes",
            "auth": "10-15 minutes"
        }
        
        for key in base_times:
            if key in issue_type:
                return base_times[key]
        
        # Adjust based on issue count
        if issue_count > 3:
            return "30-60 minutes"
        elif issue_count > 1:
            return "20-40 minutes"
        else:
            return "10-20 minutes"
    
    def _get_generic_ai_solution(self, log_content: str) -> Dict[str, Any]:
        """Generic AI-based solution when specific patterns aren't clear"""
        return {
            "title": "AI-Guided System Resolution",
            "steps": [
                "1. Analyze error patterns and frequency in the logs",
                "2. Identify the most critical issues affecting functionality",
                "3. Apply targeted fixes based on error classification",
                "4. Test each fix incrementally to ensure stability",
                "5. Monitor system behavior after implementing changes"
            ],
            "code_example": '''# AI-GUIDED RESOLUTION
echo "🤖 Applying AI-recommended fixes..."

# Smart log analysis
grep -i "error\\|failed\\|exception" <<< "$LOG_CONTENT" | sort | uniq -c | sort -nr | head -10

# System health verification
kubectl get all --all-namespaces 2>/dev/null | grep -v Running | grep -v Completed || \\
docker ps -a | grep -v Up || \\
systemctl --failed

# Apply intelligent fixes based on patterns
echo "✅ AI analysis complete - review findings above"
''',
            "estimated_time": "15-30 minutes",
            "success_rate": 0.82,
            "pattern_id": f"ai_generic_{hash(log_content) % 10000}",
            "ai_generated": True
        }
    
    # Compatibility methods for existing code
    def get_learning_stats(self) -> Dict:
        """Get learning statistics from pattern recognition system"""
        return self.pattern_recognition.vector_search.get_learning_stats()
    
    def provide_feedback(self, analysis_id: str, feedback_data: Dict) -> Dict:
        """Store feedback for solution effectiveness"""
        try:
            self.pattern_recognition.vector_search.record_solution_feedback(
                pattern_id=analysis_id,
                solution_id=feedback_data.get("solution_id", "main"),
                rating=feedback_data.get("rating", "good"),
                helpful=feedback_data.get("helpful", True),
                feedback=feedback_data.get("feedback_text", "")
            )
            return {"status": "success", "message": "Feedback recorded"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

# Global instance for compatibility
ai_analyzer = SimplifiedAIAnalyzer()
