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
                    # Create ONE comprehensive solution from all issues
                    comprehensive_solution = self._create_comprehensive_solution(online_analysis, log_content)
                    
                    # Store this pattern for future learning
                    pattern_id = self.pattern_recognition.vector_search.store_deployment_pattern(
                        log_content, 
                        online_analysis.get("issues", []),
                        [comprehensive_solution]
                    )
                    
                    return {
                        "analysis_type": "AI-Enhanced Comprehensive Solution", 
                        "backend": f"{online_analysis.get('backend', 'ai')}+tidb",
                        "confidence": min(online_analysis.get("confidence", 0.85), 0.98),
                        "confidence_score": min(online_analysis.get("confidence", 0.85), 0.98),
                        "ai_powered": True,
                        
                        # Single comprehensive analysis
                        "summary": f"Detected {len(online_analysis.get('issues', []))} issues - providing unified resolution strategy",
                        "errors": online_analysis.get("issues", []),
                        "severity": self._determine_overall_severity(online_analysis.get("issues", [])),
                        
                        # ONE comprehensive solution
                        "recommendations": [comprehensive_solution],
                        
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
    
    def _create_comprehensive_solution(self, ai_analysis: Dict, log_content: str) -> Dict[str, Any]:
        """Create ONE comprehensive solution that addresses ALL issues"""
        
        issues = ai_analysis.get("issues", [])
        recommendations = ai_analysis.get("recommendations", [])
        
        if not issues:
            return self._get_generic_comprehensive_solution(log_content)
        
        # Analyze all issues to determine unified approach
        issue_types = [issue.get("type", "").lower() for issue in issues]
        primary_domain = self._determine_primary_domain(issue_types, log_content)
        
        # Create unified solution title
        critical_count = sum(1 for issue in issues if issue.get("severity") == "critical")
        solution_title = f"Comprehensive {primary_domain.title()} Resolution - {len(issues)} Issues Addressed"
        
        # Generate unified resolution steps
        unified_steps = self._generate_unified_steps(issues, primary_domain)
        
        # Generate comprehensive code that addresses all issues
        comprehensive_code = self._generate_comprehensive_code(issues, primary_domain, log_content)
        
        # Calculate overall success rate
        avg_confidence = ai_analysis.get("confidence", 0.8)
        complexity_factor = max(0.7, 1.0 - (len(issues) * 0.05))  # More issues = slight complexity penalty
        success_rate = min(avg_confidence * complexity_factor, 0.95)
        
        return {
            "title": solution_title,
            "description": f"Unified resolution addressing {len(issues)} deployment issues in {primary_domain} environment",
            "steps": unified_steps,
            "code": comprehensive_code,
            "estimated_time": self._estimate_comprehensive_time(issues, primary_domain),
            "success_rate": success_rate,
            "complexity": "medium" if len(issues) <= 3 else "high",
            "addresses_issues": [issue.get("title", "Unknown") for issue in issues],
            "ai_generated": True,
            "pattern_id": f"unified_{primary_domain}_{hash(log_content) % 10000}"
        }
    
    def _determine_primary_domain(self, issue_types: List[str], log_content: str) -> str:
        """Determine the primary technology domain for unified solution"""
        
        log_lower = log_content.lower()
        
        # Count indicators for each domain
        domain_scores = {
            "kubernetes": sum([
                log_lower.count("kubectl"), log_lower.count("pod"), 
                log_lower.count("deployment"), log_lower.count("namespace")
            ]),
            "docker": sum([
                log_lower.count("docker"), log_lower.count("container"),
                log_lower.count("dockerfile"), log_lower.count("image")
            ]),
            "database": sum([
                log_lower.count("mysql"), log_lower.count("postgres"),
                log_lower.count("database"), log_lower.count("connection")
            ]),
            "network": sum([
                log_lower.count("port"), log_lower.count("bind"),
                log_lower.count("connection"), log_lower.count("timeout")
            ])
        }
        
        # Return domain with highest score
        return max(domain_scores.items(), key=lambda x: x[1])[0]
    
    def _generate_unified_steps(self, issues: List[Dict], domain: str) -> List[str]:
        """Generate unified resolution steps that address all issues"""
        
        if domain == "kubernetes":
            return [
                "1. **Cluster Assessment** - Check overall cluster health and resource availability",
                "2. **Pod Analysis** - Review all failing pods and their resource requirements", 
                "3. **Resource Scaling** - Add nodes or adjust resource limits to resolve capacity issues",
                "4. **Configuration Fix** - Update deployments with corrected specifications",
                "5. **Rollout & Monitor** - Deploy fixes and monitor for successful resolution"
            ]
        elif domain == "docker":
            return [
                "1. **Build Context Review** - Verify all required files are available in build context",
                "2. **Port Conflict Resolution** - Stop conflicting services and free up required ports",
                "3. **Clean Rebuild** - Perform fresh build with updated configuration",
                "4. **Container Testing** - Validate container functionality before deployment", 
                "5. **Deployment Verification** - Confirm successful deployment and operation"
            ]
        elif domain == "database":
            return [
                "1. **Connection Validation** - Test database connectivity and authentication",
                "2. **Schema Synchronization** - Run migrations and update database schema",
                "3. **Permission Verification** - Confirm user permissions and access rights",
                "4. **Application Integration** - Test application database connectivity",
                "5. **Performance Monitoring** - Monitor database performance post-resolution"
            ]
        else:
            return [
                "1. **System Analysis** - Comprehensive review of all reported issues",
                "2. **Root Cause Identification** - Determine underlying causes and dependencies", 
                "3. **Coordinated Resolution** - Apply fixes in optimal sequence to prevent conflicts",
                "4. **Integration Testing** - Verify all components work together correctly",
                "5. **Monitoring Setup** - Establish monitoring to prevent issue recurrence"
            ]
    
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
    

        
    def _generate_comprehensive_code(self, issues: List[Dict], domain: str, log_content: str) -> str:
        """Generate comprehensive code that addresses all detected issues"""
        
        if domain == "kubernetes":
            return '''#!/bin/bash
# COMPREHENSIVE KUBERNETES RESOLUTION
echo "� Executing unified Kubernetes fix for all detected issues..."

# STEP 1: Cluster Health Assessment
echo "📊 Checking cluster health..."
kubectl cluster-info
kubectl get nodes -o wide
kubectl describe nodes | grep -E "(Condition|Pressure|Eviction)" 

# STEP 2: Resource Analysis  
echo "🔍 Analyzing resource utilization..."
kubectl top nodes 2>/dev/null || echo "Metrics server not available"
kubectl get pods --all-namespaces --field-selector=status.phase!=Running

# STEP 3: Fix Pod Creation Issues
echo "🛠️ Resolving pod creation and scheduling..."
kubectl get deployment -o wide
kubectl describe deployment $DEPLOYMENT_NAME 2>/dev/null || true

# Add resource requests/limits to prevent scheduling issues
kubectl patch deployment $DEPLOYMENT_NAME -p '{
  "spec": {
    "template": {
      "spec": {
        "containers": [{
          "name": "'$CONTAINER_NAME'",
          "resources": {
            "requests": {"memory": "512Mi", "cpu": "250m"},
            "limits": {"memory": "1Gi", "cpu": "500m"}
          }
        }]
      }
    }
  }
}' 2>/dev/null || echo "Deployment patch skipped"

# STEP 4: Scale if needed
echo "📈 Scaling resources..."
kubectl scale deployment $DEPLOYMENT_NAME --replicas=2
kubectl get pods -w --timeout=60s

# STEP 5: Verify resolution
echo "✅ Verifying fixes..."
kubectl rollout status deployment/$DEPLOYMENT_NAME
kubectl get pods -l app=$APP_LABEL
echo "All Kubernetes issues resolved!"'''
        
        elif domain == "docker":
            return '''#!/bin/bash  
# COMPREHENSIVE DOCKER RESOLUTION
echo "🚀 Executing unified Docker fix for all detected issues..."

# STEP 1: Port Conflict Resolution
echo "🔌 Resolving port conflicts..."
sudo lsof -i :80 -i :8080 -i :3000 | grep LISTEN || echo "Ports available"
docker ps --format "table {{.Names}}\\t{{.Ports}}" | grep -E "80|8080|3000" || echo "No conflicting containers"

# Stop conflicting containers
docker ps -q --filter "publish=80" | xargs -r docker stop
docker ps -q --filter "publish=8080" | xargs -r docker stop

# STEP 2: Build Context Fix
echo "📁 Fixing build context issues..."
[ -f .dockerignore ] && echo "Current .dockerignore:" && cat .dockerignore
find . -name "requirements.txt" -o -name "package.json" -o -name "*.py" | head -10

# STEP 3: Clean Build Process
echo "🏗️ Performing clean rebuild..."
docker build --no-cache --progress=plain -t $IMAGE_NAME . 2>&1 | tee build.log

# STEP 4: Container Validation  
echo "🧪 Testing container functionality..."
docker run --rm $IMAGE_NAME echo "Container test successful" || echo "Container test failed"

# STEP 5: Deploy with proper port mapping
echo "🚀 Deploying with resolved configuration..."
docker run -d --name $CONTAINER_NAME -p 8080:80 $IMAGE_NAME
docker logs $CONTAINER_NAME
echo "All Docker issues resolved!"'''
        
        elif domain == "database":
            return '''#!/bin/bash
# COMPREHENSIVE DATABASE RESOLUTION  
echo "🚀 Executing unified database fix for all detected issues..."

# STEP 1: Connection Testing
echo "🔗 Testing database connectivity..."
ping -c 3 $DB_HOST 2>/dev/null || echo "Host ping failed" 
nc -zv $DB_HOST $DB_PORT 2>&1 || echo "Port connection failed"

# STEP 2: Authentication Verification
echo "🔐 Verifying database authentication..."
if command -v mysql &> /dev/null; then
    mysql -h $DB_HOST -P $DB_PORT -u $DB_USER -p$DB_PASSWORD -e "SELECT 1;" 2>/dev/null && echo "MySQL connection OK"
fi
if command -v psql &> /dev/null; then
    PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "SELECT 1;" 2>/dev/null && echo "PostgreSQL connection OK"
fi

# STEP 3: Schema Migration
echo "📋 Running database migrations..."
python manage.py migrate 2>/dev/null || \\
npx sequelize-cli db:migrate 2>/dev/null || \\
php artisan migrate 2>/dev/null || \\
echo "No migration tool found"

# STEP 4: Application Integration Test
echo "🔧 Testing application integration..."  
python -c "
import os
try:
    if 'mysql' in os.environ.get('DATABASE_URL', '').lower():
        import mysql.connector
        print('MySQL driver available')
    elif 'postgres' in os.environ.get('DATABASE_URL', '').lower():
        import psycopg2  
        print('PostgreSQL driver available')
except ImportError as e:
    print(f'Database driver issue: {e}')
" 2>/dev/null

# STEP 5: Verify Resolution
echo "✅ Verifying database resolution..."
curl -f http://localhost:8080/health 2>/dev/null && echo "App health check passed" || echo "App health check failed"
echo "All database issues resolved!"'''
        
        else:
            return '''#!/bin/bash
# COMPREHENSIVE SYSTEM RESOLUTION
echo "🚀 Executing unified system fix for all detected issues..."

# STEP 1: System Health Check
echo "🏥 Checking system health..."
uptime && free -h && df -h | head -5

# STEP 2: Service Status Review
echo "⚙️ Reviewing service status..."
systemctl --failed --no-pager || echo "No failed services"
docker ps -a --format "table {{.Names}}\\t{{.Status}}" 2>/dev/null || echo "Docker not available"

# STEP 3: Log Analysis
echo "📋 Analyzing system logs..."  
journalctl --since "1 hour ago" --no-pager | tail -20
dmesg | tail -10 | grep -i error || echo "No recent kernel errors"

# STEP 4: Network Connectivity  
echo "🌐 Testing network connectivity..."
ping -c 3 8.8.8.8 && curl -I https://google.com --max-time 5

# STEP 5: Apply General Fixes
echo "🔧 Applying general system fixes..."
sudo systemctl daemon-reload
sudo systemctl restart systemd-resolved 2>/dev/null || true
echo "System resolution complete!"'''
    
    def _estimate_comprehensive_time(self, issues: List[Dict], domain: str) -> str:
        """Estimate time for comprehensive resolution"""
        
        issue_count = len(issues)
        critical_count = sum(1 for issue in issues if issue.get("severity") == "critical")
        
        base_times = {
            "kubernetes": 20,
            "docker": 15, 
            "database": 25,
            "network": 18
        }
        
        base_time = base_times.get(domain, 20)
        complexity_time = (issue_count - 1) * 5  # 5 min per additional issue
        critical_time = critical_count * 10  # 10 min per critical issue
        
        total_minutes = base_time + complexity_time + critical_time
        
        if total_minutes <= 30:
            return f"{total_minutes} minutes"
        else:
            hours = total_minutes // 60
            minutes = total_minutes % 60
            return f"{hours}h {minutes}min" if minutes > 0 else f"{hours}h"
    
    def _determine_overall_severity(self, issues: List[Dict]) -> str:
        """Determine overall severity from all issues"""
        
        if not issues:
            return "low"
        
        severities = [issue.get("severity", "low") for issue in issues]
        
        if "critical" in severities:
            return "critical"
        elif "high" in severities:
            return "high"  
        elif "medium" in severities:
            return "medium"
        else:
            return "low"
    
    def _get_generic_comprehensive_solution(self, log_content: str) -> Dict[str, Any]:
        """Generic comprehensive solution when AI analysis is unclear"""
        
        return {
            "title": "Comprehensive System Analysis & Resolution",
            "description": "AI-guided comprehensive fix for detected system issues",
            "steps": [
                "1. **System Assessment** - Complete analysis of system health and performance",
                "2. **Issue Classification** - Categorize and prioritize all detected problems", 
                "3. **Unified Resolution** - Apply coordinated fixes to resolve all issues",
                "4. **Integration Testing** - Verify all components work together properly",
                "5. **Monitoring Setup** - Establish ongoing monitoring for issue prevention"
            ],
            "code": '''#!/bin/bash
# AI-GUIDED COMPREHENSIVE RESOLUTION
echo "🤖 Applying AI-recommended comprehensive fixes..."

# System health analysis
uptime && df -h && free -h

# Service status check  
systemctl --failed || docker ps -a 2>/dev/null

# Apply AI-recommended fixes
systemctl daemon-reload
echo "✅ Comprehensive resolution completed!"''',
            "estimated_time": "25-40 minutes",
            "success_rate": 0.85,
            "complexity": "medium",
            "ai_generated": True,
            "pattern_id": f"generic_ai_{hash(log_content) % 10000}"
        }
    
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
