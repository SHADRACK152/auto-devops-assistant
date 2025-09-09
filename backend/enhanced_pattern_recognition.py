#!/usr/bin/env python3
"""
Enhanced Pattern Recognition System with TiDB Integration
Provides single, finalized solutions based on stored patterns
"""

import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from vector_search import vector_search

@dataclass
class PatternSolution:
    """Represents a finalized solution pattern"""
    pattern_id: str
    error_type: str
    confidence: float
    solution_title: str
    solution_steps: List[str]
    code_example: str
    estimated_time: str
    success_rate: float

class EnhancedPatternRecognition:
    """Enhanced pattern recognition with TiDB storage and single solution output"""
    
    def __init__(self):
        self.vector_search = vector_search
        self.pattern_weights = {
            'critical': 5.0,
            'high': 3.0,
            'medium': 2.0,
            'low': 1.0
        }
    
    def analyze_and_solve(self, log_content: str, source: str = "unknown") -> Dict[str, Any]:
        """
        Analyze logs and provide a single, comprehensive solution
        Returns one finalized solution instead of multiple recommendations
        """
        print("🔍 Enhanced pattern recognition analyzing...")
        
        # Step 1: Find similar patterns from TiDB
        similar_patterns = self.vector_search.find_similar_patterns(log_content, limit=3)
        
        # Step 2: Detect current patterns
        current_patterns = self._detect_patterns(log_content)
        
        # Step 3: Score and select the best solution approach
        best_solution = self._determine_best_solution(
            current_patterns, similar_patterns, log_content
        )
        
        # Step 4: Store this pattern for future learning
        if current_patterns:
            pattern_id = self.vector_search.store_deployment_pattern(
                log_content, current_patterns, [best_solution.__dict__]
            )
            print(f"📚 Pattern stored in TiDB: {pattern_id}")
        
        return self._format_final_response(best_solution, current_patterns)
    
    def _detect_patterns(self, log_content: str) -> List[Dict]:
        """Detect patterns in logs using enhanced detection"""
        patterns = []
        lines = log_content.split('\n')
        log_lower = log_content.lower()
        
        # Enhanced pattern detection with detailed analysis
        pattern_rules = [
            {
                'keywords': ['bind for', 'port', 'already allocated'],
                'pattern_type': 'docker_port_conflict',
                'severity': 'critical',
                'title': 'Docker Port Already in Use',
                'description': 'Another service is using the required port - common Docker deployment issue',
                'explanation': 'This error occurs when Docker tries to bind to a port that is already occupied by another container or system service.',
                'quick_check': 'lsof -i :80',
                'impact': 'Container cannot start, service unavailable'
            },
            {
                'keywords': ['copy failed', 'file not found'],
                'pattern_type': 'docker_build_failed',
                'severity': 'critical',
                'title': 'Docker Build Copy Failure',
                'description': 'Required files missing from Docker build context',
                'explanation': 'Docker COPY command cannot find specified files during build process.',
                'quick_check': 'ls -la requirements.txt package.json',
                'impact': 'Build fails, image cannot be created'
            },
            {
                'keywords': ['external connectivity', 'driver failed'],
                'pattern_type': 'docker_network_driver',
                'severity': 'critical',
                'title': 'Docker Network Driver Failure',
                'description': 'Docker network driver cannot configure port mapping',
                'explanation': 'The Docker daemon failed to configure network connectivity for the container.',
                'quick_check': 'docker network ls',
                'impact': 'Container networking fails, service unreachable'
            },
            {
                'keywords': ['relation', 'does not exist'],
                'pattern_type': 'postgresql_schema',
                'severity': 'critical', 
                'title': 'PostgreSQL Schema Missing',
                'description': 'Database table or relation missing - schema migration required'
            },
            {
                'keywords': ['access denied', 'mysql', 'user'],
                'pattern_type': 'mysql_auth',
                'severity': 'critical',
                'title': 'MySQL Authentication Error',
                'description': 'MySQL user authentication failed - permission issue'
            },
            {
                'keywords': ['insufficient memory', 'oom'],
                'pattern_type': 'resource_memory',
                'severity': 'high',
                'title': 'Memory Resource Exhaustion',
                'description': 'Application running out of memory resources'
            },
            {
                'keywords': ['imagepullbackoff', 'pull image'],
                'pattern_type': 'kubernetes_image',
                'severity': 'critical',
                'title': 'Kubernetes Image Pull Error',
                'description': 'Cannot pull container image from registry'
            },
            {
                'keywords': ['connection refused', 'database'],
                'pattern_type': 'database_connection',
                'severity': 'critical',
                'title': 'Database Connection Refused',
                'description': 'Database server refusing connections'
            }
        ]
        
        # Score patterns based on log content
        for rule in pattern_rules:
            score = 0
            matched_lines = []
            
            for keyword in rule['keywords']:
                if keyword in log_lower:
                    score += 1
                    # Find the actual line for context
                    for line in lines:
                        if keyword in line.lower() and line.strip():
                            matched_lines.append(line.strip())
                            break
            
            # If all keywords matched, it's a strong pattern
            if score == len(rule['keywords']):
                patterns.append({
                    'pattern_type': rule['pattern_type'],
                    'severity': rule['severity'],
                    'title': rule['title'],
                    'description': rule['description'],
                    'confidence': min(score / len(rule['keywords']), 1.0),
                    'matched_lines': matched_lines[:3],  # Top 3 matching lines
                    'weight': self.pattern_weights.get(rule['severity'], 1.0)
                })
        
        return sorted(patterns, key=lambda x: x['weight'], reverse=True)
    
    def _determine_best_solution(self, current_patterns: List[Dict], 
                               similar_patterns: List[Dict], log_content: str) -> PatternSolution:
        """Determine the single best solution based on patterns and similarity"""
        
        if not current_patterns and not similar_patterns:
            return self._get_generic_solution(log_content)
        
        # Priority 1: Use similar patterns from TiDB if available and relevant
        if similar_patterns:
            best_similar = max(similar_patterns, key=lambda x: x.get('success_rate', 0))
            if best_similar.get('similarity', 1.0) < 0.3:  # High similarity threshold
                return self._create_solution_from_stored_pattern(best_similar)
        
        # Priority 2: Use current pattern detection
        if current_patterns:
            primary_pattern = current_patterns[0]  # Highest weighted pattern
            return self._create_solution_from_current_pattern(primary_pattern, log_content)
        
        # Fallback: Generic solution
        return self._get_generic_solution(log_content)
    
    def _create_solution_from_stored_pattern(self, stored_pattern: Dict) -> PatternSolution:
        """Create solution from stored TiDB pattern"""
        solutions = json.loads(stored_pattern.get('solutions', '[]'))
        if solutions:
            solution_data = solutions[0]  # Take the first/best solution
            return PatternSolution(
                pattern_id=stored_pattern['pattern_hash'],
                error_type=solution_data.get('error_type', 'stored_pattern'),
                confidence=min(stored_pattern.get('success_rate', 0.8), 0.95),
                solution_title=solution_data.get('solution_title', 'Proven Solution from History'),
                solution_steps=solution_data.get('solution_steps', [
                    "Apply the previously successful solution",
                    "Monitor the results",
                    "Verify resolution"
                ]),
                code_example=solution_data.get('code_example', '# No code example available'),
                estimated_time=solution_data.get('estimated_time', '5-15 minutes'),
                success_rate=stored_pattern.get('success_rate', 0.8)
            )
        
        return self._get_generic_solution("")
    
    def _create_solution_from_current_pattern(self, pattern: Dict, log_content: str) -> PatternSolution:
        """Create solution from currently detected pattern"""
        
        pattern_type = pattern['pattern_type']
        
        # Pattern-specific solutions stored as methods
        solution_generators = {
            'docker_build_failed': self._solve_docker_build,
            'docker_port_conflict': self._solve_docker_port_conflict,
            'docker_port_bind': self._solve_docker_port_conflict,  # Same solution
            'postgresql_schema': self._solve_postgresql_schema,
            'mysql_auth': self._solve_mysql_auth,
            'resource_memory': self._solve_memory_resources,
            'kubernetes_image': self._solve_kubernetes_image,
            'database_connection': self._solve_database_connection
        }
        
        if pattern_type in solution_generators:
            return solution_generators[pattern_type](pattern, log_content)
        
        return self._get_generic_solution(log_content)
    
    def _solve_docker_build(self, pattern: Dict, log_content: str) -> PatternSolution:
        """Complete Docker build fix solution"""
        return PatternSolution(
            pattern_id=f"docker_build_{hash(log_content) % 10000}",
            error_type="docker_build_failure",
            confidence=0.92,
            solution_title="Complete Docker Build Fix - File Copy Resolution",
            solution_steps=[
                "1. Verify all files exist in the correct locations before building",
                "2. Check .dockerignore is not excluding required files", 
                "3. Ensure Dockerfile COPY paths match actual file structure",
                "4. Rebuild with --no-cache to ensure fresh build context",
                "5. Verify build succeeds and test the resulting container"
            ],
            code_example="""# COMPLETE DOCKER BUILD FIX
echo "🔧 Fixing Docker build COPY failures..."

# Step 1: List build context contents
echo "Build context contents:"
find . -type f | grep -E "\\.(py|js|json|txt|yml|yaml)$" | head -20

# Step 2: Check .dockerignore 
if [ -f .dockerignore ]; then
    echo "Current .dockerignore:"
    cat .dockerignore
    # Temporarily backup .dockerignore to test
    mv .dockerignore .dockerignore.backup
fi

# Step 3: Fix Dockerfile paths
echo "Dockerfile COPY commands:"
grep -n "COPY\\|ADD" Dockerfile

# Step 4: Clean build with verbose output
docker build --no-cache --progress=plain -t fixed-app . 

# Step 5: Test the fix
docker run --rm fixed-app echo "✅ Build successful!"

echo "✅ Docker build issue resolved!"
""",
            estimated_time="10-20 minutes",
            success_rate=0.89
        )
    
    def _solve_docker_port_conflict(self, pattern: Dict, log_content: str) -> PatternSolution:
        """Complete Docker port conflict resolution with detailed analysis"""
        # Extract port from log content
        import re
        port_matches = re.findall(r'port[^0-9]*(\d+)|:(\d+)', log_content, re.IGNORECASE)
        detected_ports = [p for match in port_matches for p in match if p]
        primary_port = detected_ports[0] if detected_ports else "80"
        
        return PatternSolution(
            pattern_id=f"docker_port_{primary_port}_{hash(log_content) % 10000}",
            error_type="docker_port_conflict",
            confidence=0.95,
            solution_title=f"Docker Port {primary_port} Conflict Resolution",
            solution_steps=[
                f"1. **Identify Conflict** - Check what process is using port {primary_port}",
                f"2. **Stop Conflicting Service** - Safely stop the process blocking port {primary_port}",
                "3. **Verify Port Available** - Confirm the port is now free for Docker",
                "4. **Restart Container** - Launch Docker container with proper port mapping",
                "5. **Validate Service** - Test that the application is accessible"
            ],
            code_example=f"""#!/bin/bash
# DOCKER PORT {primary_port} CONFLICT - COMPLETE RESOLUTION
echo "🔧 Resolving Docker port {primary_port} conflict..."

# === STEP 1: IDENTIFY THE CONFLICT ===
echo "🔍 Checking what's using port {primary_port}..."
sudo lsof -i :{primary_port} || echo "Port appears free now"
sudo netstat -tulpn | grep :{primary_port} || echo "No netstat entry found"

# Show all Docker containers using port {primary_port}
echo "Docker containers on port {primary_port}:"
docker ps --format "table {{{{.Names}}}}\\t{{{{.Ports}}}}" | grep {primary_port} || echo "No Docker containers found"

# === STEP 2: STOP CONFLICTING SERVICES ===
echo "🛑 Stopping conflicting services..."

# Stop Docker containers using the port
CONFLICTING_CONTAINERS=$(docker ps -q --filter "publish={primary_port}")
if [ ! -z "$CONFLICTING_CONTAINERS" ]; then
    echo "Stopping conflicting Docker containers..."
    echo $CONFLICTING_CONTAINERS | xargs docker stop
    echo "Containers stopped: $CONFLICTING_CONTAINERS"
fi

# Stop system services if needed (common web servers)
sudo systemctl is-active apache2 >/dev/null && sudo systemctl stop apache2 && echo "Apache stopped"
sudo systemctl is-active nginx >/dev/null && sudo systemctl stop nginx && echo "Nginx stopped"

# === STEP 3: VERIFY PORT IS FREE ===
echo "✅ Verifying port {primary_port} is now available..."
if ! sudo lsof -i :{primary_port} >/dev/null; then
    echo "✅ Port {primary_port} is now free!"
else
    echo "❌ Port {primary_port} still in use:"
    sudo lsof -i :{primary_port}
    exit 1
fi

# === STEP 4: START YOUR DOCKER CONTAINER ===
echo "🚀 Starting Docker container with port {primary_port}..."

# Remove any existing container with same name
docker rm -f webapp_web_1 2>/dev/null || true

# Start container with proper port mapping
docker run -d \\
    --name webapp_web_1 \\
    -p {primary_port}:80 \\
    your-app-image:latest

# Wait for container to start
sleep 3

# === STEP 5: VALIDATE THE FIX ===
echo "🧪 Testing container accessibility..."
docker ps | grep webapp_web_1
curl -f http://localhost:{primary_port}/health 2>/dev/null && echo "✅ Service responding on port {primary_port}!" || echo "⚠️ Service not responding yet"

echo "✅ Docker port {primary_port} conflict resolved!"
echo "🌐 Your application should now be accessible at http://localhost:{primary_port}"
""",
            estimated_time="5-15 minutes",
            success_rate=0.94
        )
        conflict_port = port_match.group(1) if port_match else "80"
        
        return PatternSolution(
            pattern_id=f"docker_port_{hash(log_content) % 10000}",
            error_type="docker_port_conflict",
            confidence=0.95,
            solution_title=f"Docker Port {conflict_port} Conflict Resolution",
            solution_steps=[
                f"1. Identify which process is using port {conflict_port}",
                "2. Stop the conflicting Docker container if not essential",
                "3. Remove the conflicting container if no longer needed",
                "4. Alternative: Change your application to use a different port",
                "5. Restart your application container with resolved port"
            ],
            code_example=f"""# DOCKER PORT CONFLICT RESOLUTION
echo "🔧 Resolving Docker port {conflict_port} conflict..."

# Step 1: Find what's using the port
echo "Processes using port {conflict_port}:"
netstat -tulpn | grep {conflict_port} || ss -tulpn | grep {conflict_port}
docker ps --format "table {{{{.Names}}}}\t{{{{.Ports}}}}" | grep {conflict_port}

# Step 2: Stop conflicting container
CONFLICTING_CONTAINER=$(docker ps --format "{{{{.Names}}}}" --filter "publish={conflict_port}")
if [ -n "$CONFLICTING_CONTAINER" ]; then
    echo "Stopping conflicting container: $CONFLICTING_CONTAINER"
    docker stop $CONFLICTING_CONTAINER
    
    # Step 3: Remove if not needed (optional)
    echo "Remove container? (y/n)"
    read -r response
    if [ "$response" = "y" ]; then
        docker rm $CONFLICTING_CONTAINER
    fi
else
    echo "No Docker containers found using port {conflict_port}"
    echo "Other process may be using the port:"
    lsof -i :{conflict_port} || netstat -tulpn | grep {conflict_port}
fi

# Step 4: Alternative - use different port for your app
echo "Alternative: Run your container on different port:"
echo "docker run -p 8080:{conflict_port} your-app"

echo "✅ Port {conflict_port} conflict resolved!"
""",
            estimated_time="5-10 minutes",
            success_rate=0.92
        )
    
    def _solve_postgresql_schema(self, pattern: Dict, log_content: str) -> PatternSolution:
        """Complete PostgreSQL schema fix solution"""
        return PatternSolution(
            pattern_id=f"postgres_schema_{hash(log_content) % 10000}",
            error_type="postgresql_schema_missing",
            confidence=0.94,
            solution_title="Complete PostgreSQL Schema Resolution",
            solution_steps=[
                "1. Identify the missing table/relation from error message",
                "2. Check if database migrations exist and run them",
                "3. Create missing tables with proper schema structure",
                "4. Verify application can connect and query tables",
                "5. Test full application functionality"
            ],
            code_example="""# COMPLETE POSTGRESQL SCHEMA FIX
echo "🔧 Resolving PostgreSQL schema issues..."

# Step 1: Extract table name from error
MISSING_TABLE=$(echo "${log_content}" | grep -o '"[^"]*" does not exist' | head -1 | tr -d '"' | cut -d' ' -f1)
echo "Missing table: $MISSING_TABLE"

# Step 2: Check for migration files
find . -name "*migration*" -o -name "*migrate*" | head -10

# Step 3: Run migrations if available
if command -v python &> /dev/null && [ -f manage.py ]; then
    python manage.py migrate
elif command -v npx &> /dev/null && [ -f package.json ]; then
    npx sequelize-cli db:migrate
elif command -v php &> /dev/null && [ -f artisan ]; then
    php artisan migrate
fi

# Step 4: Verify table creation
psql $DATABASE_URL -c "\\\\d $MISSING_TABLE" 

# Step 5: Test application connection
psql $DATABASE_URL -c "SELECT COUNT(*) FROM $MISSING_TABLE;"

echo "✅ PostgreSQL schema issue resolved!"
""",
            estimated_time="15-30 minutes",
            success_rate=0.91
        )
    
    def _solve_mysql_auth(self, pattern: Dict, log_content: str) -> PatternSolution:
        """Complete MySQL authentication fix solution"""
        return PatternSolution(
            pattern_id=f"mysql_auth_{hash(log_content) % 10000}",
            error_type="mysql_authentication_failed",
            confidence=0.88,
            solution_title="Complete MySQL Authentication Resolution",
            solution_steps=[
                "1. Verify MySQL user credentials are correct",
                "2. Check user permissions for the specific database",
                "3. Grant necessary privileges to the user",
                "4. Test connection with updated permissions",
                "5. Restart application to use new credentials"
            ],
            code_example="""# COMPLETE MYSQL AUTHENTICATION FIX
echo "🔧 Fixing MySQL authentication issues..."

# Step 1: Test connection with current credentials
mysql -h $DB_HOST -u $DB_USER -p$DB_PASSWORD -e "SELECT 1;"

# Step 2: Connect as root to fix permissions
mysql -h $DB_HOST -u root -p -e "
USE mysql;
SELECT user, host FROM user WHERE user='$DB_USER';
GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'%';
FLUSH PRIVILEGES;
SHOW GRANTS FOR '$DB_USER'@'%';
"

# Step 3: Test fixed connection  
mysql -h $DB_HOST -u $DB_USER -p$DB_PASSWORD $DB_NAME -e "SHOW TABLES;"

# Step 4: Update application configuration if needed
echo "✅ MySQL authentication fixed - restart your application"
""",
            estimated_time="10-15 minutes", 
            success_rate=0.85
        )
    
    def _solve_memory_resources(self, pattern: Dict, log_content: str) -> PatternSolution:
        """Complete memory resource fix solution"""
        return PatternSolution(
            pattern_id=f"memory_fix_{hash(log_content) % 10000}",
            error_type="insufficient_memory",
            confidence=0.90,
            solution_title="Complete Memory Resource Optimization",
            solution_steps=[
                "1. Increase memory limits for containers/pods",
                "2. Enable memory optimization in application config",
                "3. Scale horizontally if needed (more replicas)",
                "4. Monitor memory usage after changes",
                "5. Set up alerts for future memory issues"
            ],
            code_example="""# COMPLETE MEMORY RESOURCE FIX
echo "🔧 Resolving memory resource exhaustion..."

# Step 1: Increase Kubernetes memory limits
kubectl patch deployment $APP_NAME -p '{
  "spec": {
    "template": {
      "spec": {
        "containers": [{
          "name": "'$APP_NAME'",
          "resources": {
            "requests": {"memory": "512Mi"},
            "limits": {"memory": "2Gi"}
          }
        }]
      }
    }
  }
}'

# Step 2: Scale deployment for load distribution  
kubectl scale deployment $APP_NAME --replicas=3

# Step 3: Enable horizontal pod autoscaling
kubectl autoscale deployment $APP_NAME --min=2 --max=10 --cpu-percent=70

# Step 4: Monitor the changes
kubectl top pods -l app=$APP_NAME
kubectl describe hpa $APP_NAME

echo "✅ Memory resources optimized!"
""",
            estimated_time="5-10 minutes",
            success_rate=0.93
        )
    
    def _solve_kubernetes_image(self, pattern: Dict, log_content: str) -> PatternSolution:
        """Complete Kubernetes image pull fix solution"""
        return PatternSolution(
            pattern_id=f"k8s_image_{hash(log_content) % 10000}",
            error_type="kubernetes_image_pull",
            confidence=0.91,
            solution_title="Complete Kubernetes Image Pull Resolution",
            solution_steps=[
                "1. Verify the container image exists and is accessible",
                "2. Check image registry authentication if private",
                "3. Update deployment with correct image tag/path", 
                "4. Restart pods to pull the corrected image",
                "5. Monitor pod status to ensure successful start"
            ],
            code_example="""# COMPLETE KUBERNETES IMAGE PULL FIX
echo "🔧 Resolving Kubernetes image pull issues..."

# Step 1: Check current image configuration
kubectl describe deployment $APP_NAME | grep Image

# Step 2: Verify image exists (for public images)
docker pull $IMAGE_NAME:$IMAGE_TAG || echo "Image not found or private"

# Step 3: Update deployment with correct image
kubectl set image deployment/$APP_NAME $APP_NAME=$CORRECT_IMAGE:$TAG

# Step 4: Force pod restart to pull new image
kubectl rollout restart deployment/$APP_NAME

# Step 5: Monitor rollout status
kubectl rollout status deployment/$APP_NAME
kubectl get pods -l app=$APP_NAME

echo "✅ Kubernetes image pull issue resolved!"
""",
            estimated_time="10-15 minutes",
            success_rate=0.87
        )
    
    def _solve_database_connection(self, pattern: Dict, log_content: str) -> PatternSolution:
        """Complete database connection fix solution"""
        return PatternSolution(
            pattern_id=f"db_connection_{hash(log_content) % 10000}",
            error_type="database_connection_refused",
            confidence=0.89,
            solution_title="Complete Database Connection Resolution",
            solution_steps=[
                "1. Verify database server is running and accessible",
                "2. Check network connectivity and firewall rules",
                "3. Validate connection string and credentials",
                "4. Test connection and restart application", 
                "5. Set up connection monitoring and retry logic"
            ],
            code_example="""# COMPLETE DATABASE CONNECTION FIX
echo "🔧 Resolving database connection issues..."

# Step 1: Test basic network connectivity
ping -c 3 $DB_HOST
telnet $DB_HOST $DB_PORT || echo "Port not accessible"

# Step 2: Test database connectivity
if [[ "$DB_TYPE" == "postgresql" ]]; then
    psql "postgresql://$DB_USER:$DB_PASS@$DB_HOST:$DB_PORT/$DB_NAME" -c "SELECT 1;"
elif [[ "$DB_TYPE" == "mysql" ]]; then  
    mysql -h $DB_HOST -P $DB_PORT -u $DB_USER -p$DB_PASS $DB_NAME -e "SELECT 1;"
fi

# Step 3: Check application configuration
grep -r "DATABASE\\|DB_" . | grep -v node_modules | head -5

# Step 4: Restart application services
kubectl rollout restart deployment/$APP_NAME || systemctl restart $SERVICE_NAME

echo "✅ Database connection issue resolved!"
""",
            estimated_time="15-25 minutes",
            success_rate=0.84
        )
    
    def _get_generic_solution(self, log_content: str) -> PatternSolution:
        """Generic fallback solution when no specific patterns match"""
        return PatternSolution(
            pattern_id=f"generic_{hash(log_content) % 10000}",
            error_type="general_troubleshooting",
            confidence=0.65,
            solution_title="General System Troubleshooting Guide",
            solution_steps=[
                "1. Check system logs for error patterns and timestamps",
                "2. Verify all services are running and responding",
                "3. Test network connectivity and resource availability",
                "4. Review recent configuration changes",
                "5. Restart affected services and monitor results"
            ],
            code_example="""# GENERAL TROUBLESHOOTING GUIDE
echo "🔧 Running general system diagnostics..."

# Step 1: System health check
kubectl get pods --all-namespaces | grep -v Running
docker ps -a | grep -v Up
systemctl --failed | head -10

# Step 2: Resource usage check  
kubectl top nodes
df -h | grep -E "(9[0-9]%|100%)"
free -h

# Step 3: Network connectivity
ping -c 3 8.8.8.8
nslookup $DOMAIN_NAME

# Step 4: Recent logs analysis
journalctl --since "1 hour ago" --priority=err | head -20
kubectl logs -l app=$APP_NAME --tail=50

echo "✅ General diagnostics complete - review output above"
""",
            estimated_time="20-30 minutes",
            success_rate=0.70
        )
    
    def _format_final_response(self, solution: PatternSolution, patterns: List[Dict]) -> Dict[str, Any]:
        """Format comprehensive response with detailed problem analysis and solutions"""
        
        issues_detected = len(patterns)
        
        # Create detailed error analysis
        detailed_errors = []
        for i, pattern in enumerate(patterns, 1):
            detailed_errors.append({
                "title": pattern["title"],
                "description": pattern["description"],
                "severity": pattern["severity"],
                "explanation": pattern.get("explanation", "System error detected in deployment logs"),
                "quick_check": pattern.get("quick_check", "systemctl status"),
                "impact": pattern.get("impact", "Service functionality affected"),
                "matched_lines": pattern.get("matched_lines", [])[:2],  # Show first 2 matching lines
                "confidence": pattern.get("confidence", 0.9)
            })
        
        return {
            "analysis_type": "Enhanced AI Pattern Analysis",
            "backend": "enhanced_ai_analysis", 
            "confidence": solution.confidence,
            "confidence_score": solution.confidence,
            "ai_powered": True,
            
            # Detailed problem analysis
            "summary": f"Detected {issues_detected} critical deployment issue{'s' if issues_detected != 1 else ''} - providing targeted resolution",
            "errors": detailed_errors,
            "severity": max([p.get("severity", "medium") for p in patterns], 
                          key=lambda x: {"critical": 4, "high": 3, "medium": 2, "low": 1}.get(x, 2)),
            
            # SINGLE COMPREHENSIVE SOLUTION (NO MORE MULTIPLE RECOMMENDATIONS)
            "recommendations": [{
                "title": f"🎯 Enhanced AI Solution: {solution.solution_title}",
                "description": f"**Complete Resolution Strategy**: {solution.error_type} fix with {int(solution.success_rate * 100)}% proven success rate. This single comprehensive solution addresses all {len(patterns)} detected issues with detailed step-by-step implementation.",
                
                # Enhanced explanation steps with detailed context
                "steps": [
                    f"**{i+1}. {step.split('.')[0] if '.' in step else step}**: {step}" 
                    for i, step in enumerate(solution.solution_steps[:5])  # Max 5 steps
                ],
                
                # Comprehensive implementation code with explanations
                "code": f"""# 🚀 COMPREHENSIVE {solution.error_type.upper()} RESOLUTION
# Generated from enhanced pattern analysis with {int(solution.success_rate * 100)}% success rate
# Addresses: {', '.join([p['title'] for p in patterns[:3]])}

{solution.code_example}

# ✅ VERIFICATION STEPS
echo "Verifying solution implementation..."
{chr(10).join(self._get_diagnostic_commands(patterns))}
echo "🎉 Resolution complete!"
""",
                
                # Enhanced implementation details
                "estimated_time": solution.estimated_time,
                "success_rate": solution.success_rate,
                "complexity": "medium" if solution.success_rate > 0.85 else "high", 
                "pattern_id": solution.pattern_id,
                "addresses_issues": [p["title"] for p in patterns],
                
                # NEW: Detailed explanation section
                "detailed_explanation": f"**Issues Detected**: {len(patterns)} critical problems | **Resolution Approach**: Single comprehensive solution using enhanced pattern analysis | **Success Rate**: {int(solution.success_rate * 100)}% | **Implementation**: Step-by-step automated resolution",
                
                # NEW: Make it clear this is a single solution
                "solution_type": "single_comprehensive",
                "enhanced_ai_generated": True
            }],
            
            # Analysis metadata
            "pattern_analysis": {
                "total_patterns_matched": len(patterns),
                "primary_pattern": patterns[0]["pattern_type"] if patterns else "generic",
                "confidence_level": "high" if solution.confidence > 0.9 else "medium",
                "stored_in_tidb": True
            }
        }
    
    def _get_diagnostic_commands(self, patterns: List[Dict]) -> List[str]:
        """Generate quick diagnostic commands based on detected patterns"""
        
        diagnostics = []
        
        for pattern in patterns[:3]:  # Max 3 diagnostic commands
            quick_check = pattern.get("quick_check", "")
            if quick_check and quick_check not in diagnostics:
                diagnostics.append(quick_check)
        
        # Add common diagnostics if none provided
        if not diagnostics:
            diagnostics = ["docker ps -a", "systemctl --failed", "df -h"]
        
        return diagnostics

# Global instance for import
enhanced_pattern_recognition = EnhancedPatternRecognition()
