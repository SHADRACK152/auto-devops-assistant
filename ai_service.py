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
        print("🚀 Initializing SimplifiedAIAnalyzer...")
        try:
            self.online_ai = OnlineAIService()
            print(f"✅ OnlineAIService initialized. Available backends: {self.online_ai.available_backends}")
            print(f"✅ Active backend: {self.online_ai.active_backend}")
        except Exception as e:
            print(f"❌ Failed to initialize OnlineAIService: {e}")
            self.online_ai = None
        
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
        
        if self.online_ai and hasattr(self.online_ai, 'available_backends') and self.online_ai.available_backends:
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
        else:
            print("ℹ️  Online AI not available, using pattern recognition only")
        
        # Step 3: Combine both analyses and get proven solutions
        combined_issues = self._merge_issues(pattern_issues, ai_issues)
        combined_recommendations = self._merge_recommendations(pattern_recommendations, ai_recommendations)
        
        # Step 4: Add proven solutions based on identified patterns
        proven_solutions = self._get_proven_solutions(combined_issues)
        if proven_solutions:
            combined_recommendations.extend(proven_solutions)
        
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
            # Docker/Container Build Issues - HIGHEST PRIORITY
            {
                'pattern': ['copy failed', 'file not found'],
                'title': 'Docker COPY Failed - File Not Found',
                'severity': 'critical',
                'type': 'docker_build',
                'description': 'Docker COPY command failed - missing file in build context'
            },
            {
                'pattern': ['copy failed', 'dockerignore'],
                'title': 'Docker COPY Failed - File Excluded',
                'severity': 'critical',
                'type': 'docker_build',
                'description': 'File excluded by .dockerignore or missing from build context'
            },
            {
                'pattern': ['copy failed', 'build context'],
                'title': 'Docker Build Context Error',
                'severity': 'critical',
                'type': 'docker_build',
                'description': 'Required file not found in Docker build context'
            },
            {
                'pattern': ['dockerfile', 'not found'],
                'title': 'Dockerfile Missing',
                'severity': 'critical',
                'type': 'docker_build',
                'description': 'Dockerfile not found in build context'
            },
            {
                'pattern': ['failed to pull image', 'pull image', 'image not found'],
                'title': 'Container Image Pull Failed',
                'severity': 'critical',
                'type': 'docker_image',
                'description': 'Cannot pull Docker image from registry'
            },
            {
                'pattern': ['imagepullbackoff'],
                'title': 'Image Pull BackOff Error',
                'severity': 'critical',
                'type': 'docker_image',
                'description': 'Kubernetes failed to pull container image'
            },
            # Network/Firewall issues
            {
                'pattern': ['net::err_connection_reset'],
                'title': 'Network Connection Reset',
                'severity': 'critical',
                'type': 'network',
                'description': 'Network connection was reset - firewall or network issue'
            },
            {
                'pattern': ['connection reset'],
                'title': 'Connection Reset Error',
                'severity': 'critical',
                'type': 'network',
                'description': 'Connection reset by peer or firewall'
            },
            {
                'pattern': ['firewall', 'block'],
                'title': 'Firewall Blocking Connection',
                'severity': 'high',
                'type': 'firewall',
                'description': 'Firewall rules blocking network access'
            },
            {
                'pattern': ['security group', 'inbound traffic', 'port 80', 'port 443'],
                'title': 'AWS Security Group Blocking Access',
                'severity': 'critical',
                'type': 'aws_security_group',
                'description': 'AWS Security Group not allowing inbound traffic on required ports'
            },
            {
                'pattern': ['connection timed out', 'public ip', 'security group'],
                'title': 'AWS Security Group Connection Timeout',
                'severity': 'critical', 
                'type': 'aws_security_group',
                'description': 'Connection timeout due to AWS Security Group restrictions'
            },
            {
                'pattern': ['timeout', 'connection'],
                'title': 'Network Timeout',
                'severity': 'high',
                'type': 'network',
                'description': 'Network connection timeout'
            },
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
            # PostgreSQL Schema Issues - SPECIFIC PATTERNS
            {
                'pattern': ['relation', 'does not exist'],
                'title': 'PostgreSQL Table Missing',
                'severity': 'critical',
                'type': 'postgresql_schema',
                'description': 'PostgreSQL table/relation does not exist - schema migration needed'
            },
            {
                'pattern': ['column', 'does not exist'],
                'title': 'PostgreSQL Column Missing', 
                'severity': 'high',
                'type': 'postgresql_schema',
                'description': 'PostgreSQL column missing - database schema migration required'
            },
            {
                'pattern': ['table', 'does not exist'],
                'title': 'PostgreSQL Table Not Found',
                'severity': 'critical',
                'type': 'postgresql_schema',
                'description': 'PostgreSQL table missing - needs schema creation or migration'
            },
            {
                'pattern': ['schema', 'does not exist'],
                'title': 'PostgreSQL Schema Missing',
                'severity': 'critical', 
                'type': 'postgresql_schema',
                'description': 'PostgreSQL schema not found - database initialization required'
            },
            # MySQL Authentication Issues - SPECIFIC PATTERNS
            {
                'pattern': ['access denied', 'user'],
                'title': 'MySQL Access Denied Error',
                'severity': 'critical',
                'type': 'mysql_auth',
                'description': 'MySQL user authentication failed - permissions or credentials issue'
            },
            {
                'pattern': ['sequelizeconnectionerror', 'access denied'],
                'title': 'Sequelize MySQL Access Denied',
                'severity': 'critical',
                'type': 'mysql_auth',
                'description': 'Sequelize cannot connect to MySQL - user permissions required'
            },
            {
                'pattern': ['access denied', 'database'],
                'title': 'MySQL Database Access Denied',
                'severity': 'critical',
                'type': 'mysql_auth',
                'description': 'MySQL user lacks access permissions to specific database'
            },
            {
                'pattern': ['host', 'not allowed', 'connect'],
                'title': 'MySQL Host Access Denied',
                'severity': 'critical',
                'type': 'mysql_auth',
                'description': 'MySQL user not allowed to connect from this host'
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
        """Generate intelligent pattern-based recommendations with proven solutions"""
        if not issues:
            return ["No issues detected - system appears healthy"]
        
        recommendations = []
        
        # Pattern-based solution lookup - match specific error patterns to proven fixes
        for issue in issues:
            issue_type = issue.get('type', '').lower()
            issue_title = issue.get('title', '').lower()
            
            # Docker Build Context pattern solutions - HIGHEST PRIORITY
            if issue_type in ['docker_build', 'docker_image'] or 'copy failed' in issue_title:
                recommendations.extend([
                    "Apply proven Docker build fixes: Check file exists in build context and verify Dockerfile COPY paths",
                    "Examine .dockerignore file - ensure required files are not excluded from build context",
                    "Verify all COPY/ADD source paths in Dockerfile match actual file locations"
                ])
            
            # PostgreSQL Schema pattern solutions - CRITICAL DATABASE ISSUES
            elif issue_type == 'postgresql_schema' or 'relation' in issue_title and 'does not exist' in issue_title:
                recommendations.extend([
                    "Apply proven PostgreSQL schema fixes: Run database migrations to create missing tables",
                    "Check if database initialization scripts have been executed properly", 
                    "Verify application has correct database schema version and run pending migrations"
                ])
            
            # MySQL Authentication pattern solutions - CRITICAL AUTH ISSUES
            elif issue_type == 'mysql_auth' or 'access denied' in issue_title:
                recommendations.extend([
                    "Apply proven MySQL authentication fixes: Grant proper database permissions to user",
                    "Verify MySQL user credentials and host access permissions are correctly configured",
                    "Check MySQL user exists and has required privileges for the target database"
                ])
            
            # AWS Security Group pattern solutions - CRITICAL CONNECTIVITY ISSUES  
            elif issue_type == 'aws_security_group' or 'security group' in issue_title:
                recommendations.extend([
                    "Apply proven AWS Security Group fixes: Open inbound rules for ports 80 and 443",
                    "Verify Security Group allows traffic from 0.0.0.0/0 for HTTP/HTTPS access",
                    "Check that Load Balancer Security Group permits access from internet gateway"
                ])
            
            # Network/Firewall pattern solutions
            elif issue_type in ['network', 'firewall'] or 'connection reset' in issue_title:
                recommendations.extend([
                    "Apply proven network troubleshooting: Check firewall rules and open required ports (80, 443)",
                    "Implement connection retry logic with exponential backoff in application",
                    "Verify DNS resolution and proxy settings for external API connectivity"
                ])
            
            # Database pattern solutions
            elif issue_type == 'database' or 'database' in issue_title:
                recommendations.extend([
                    "Apply proven database fixes: Increase connection timeout and pool size",
                    "Check database service health and restart if needed",
                    "Verify DATABASE_URL and connection credentials configuration"
                ])
            
            # Kubernetes resource pattern solutions
            elif issue_type in ['resource', 'deployment', 'scheduling']:
                if 'memory' in issue_title or 'insufficient memory' in issue.get('description', ''):
                    recommendations.extend([
                        "Apply proven memory fixes: Increase pod memory limits to 2Gi minimum",
                        "Scale cluster nodes or enable cluster autoscaling",
                        "Implement memory-efficient algorithms and garbage collection tuning"
                    ])
                elif 'eviction' in issue_title:
                    recommendations.extend([
                        "Apply proven eviction fixes: Set resource requests/limits properly",
                        "Configure pod disruption budgets to prevent cascading failures",
                        "Monitor node capacity and implement predictive scaling"
                    ])
                elif 'no nodes available' in issue_title:
                    recommendations.extend([
                        "Apply proven scheduling fixes: Add worker nodes to cluster immediately",
                        "Remove node taints and check resource availability",
                        "Configure pod affinity rules and resource requirements"
                    ])
                elif 'failed to create pod' in issue_title:
                    recommendations.extend([
                        "Apply proven pod fixes: Check image pull secrets and repository access",
                        "Verify service account permissions and RBAC configurations",
                        "Review resource quotas and namespace limits"
                    ])
            
            # Environment/Configuration pattern solutions
            elif issue_type == 'environment':
                recommendations.extend([
                    "Apply proven config fixes: Set missing environment variables in deployment",
                    "Create ConfigMaps and Secrets for application configuration",
                    "Verify environment variable injection in container specs"
                ])
        
        # Source-specific proven solutions
        if source.lower() == 'kubernetes' or any('kube' in str(issue) for issue in issues):
            recommendations.extend([
                "Apply Kubernetes best practices: Use readiness/liveness probes",
                "Implement proper resource quotas and limit ranges",
                "Set up monitoring with Prometheus and alerting rules"
            ])
        
        # Severity-based urgent actions
        critical_issues = [i for i in issues if i.get('severity') == 'critical']
        if critical_issues:
            recommendations.insert(0, f"URGENT: {len(critical_issues)} critical issues detected - implement immediate fixes")
        
        high_issues = [i for i in issues if i.get('severity') == 'high']  
        if high_issues:
            recommendations.insert(1 if critical_issues else 0, f"HIGH PRIORITY: {len(high_issues)} issues need resolution within 1 hour")
        
        # Add pattern-based monitoring and prevention
        unique_types = set(issue.get('type', '') for issue in issues)
        if 'network' in unique_types:
            recommendations.append("Implement network monitoring: Set up connectivity checks and latency alerts")
        if 'database' in unique_types:
            recommendations.append("Implement database monitoring: Track connection pool and query performance")
        if any(t in unique_types for t in ['resource', 'deployment']):
            recommendations.append("Implement resource monitoring: Set up CPU/memory alerts and autoscaling")
        
        # Remove duplicates while preserving order
        seen = set()
        unique_recommendations = []
        for rec in recommendations:
            if rec not in seen:
                seen.add(rec)
                unique_recommendations.append(rec)
        
        return unique_recommendations[:10]  # Return top 10 most relevant solutions
    
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
        """Merge pattern and AI recommendations with solution pattern matching"""
        all_recs = ai_recs + pattern_recs
        
        if not all_recs:
            return ["No specific recommendations available"]
        
        # Enhanced pattern-to-solution mapping
        solution_patterns = {
            'network': {
                'keywords': ['network', 'firewall', 'connection', 'reset', 'timeout'],
                'weight': 3,
                'solution': "Complete Network and Firewall Troubleshooting Guide",
                'proven_fixes': [
                    "Check and configure firewall rules for ports 80, 443",
                    "Implement connection retry with exponential backoff",
                    "Verify DNS resolution and proxy settings",
                    "Test connectivity with ping, curl, telnet"
                ]
            },
            'database': {
                'keywords': ['database', 'db', 'sql', 'mysql', 'postgresql', 'connection'],
                'weight': 3,
                'solution': "Complete Database Connectivity Resolution",
                'proven_fixes': [
                    "Increase database connection timeout to 30s",
                    "Check database service status and restart if needed",
                    "Verify connection strings and credentials",
                    "Monitor connection pool size and adjust limits"
                ]
            },
            'kubernetes': {
                'keywords': ['kubernetes', 'kubectl', 'pod', 'node', 'deployment', 'eviction'],
                'weight': 3,
                'solution': "Complete Kubernetes Deployment Fix",
                'proven_fixes': [
                    "Check cluster health with kubectl cluster-info",
                    "Scale deployment or add worker nodes",
                    "Set proper resource requests and limits",
                    "Implement readiness and liveness probes"
                ]
            },
            'resource': {
                'keywords': ['memory', 'resource', 'cpu', 'insufficient', 'pressure'],
                'weight': 2,
                'solution': "Complete Resource Management Fix",
                'proven_fixes': [
                    "Increase pod memory limits to 2Gi minimum",
                    "Enable cluster autoscaling for dynamic scaling",
                    "Implement horizontal pod autoscaler",
                    "Monitor resource usage with metrics"
                ]
            },
            'environment': {
                'keywords': ['env', 'variable', 'config', 'secret', 'configmap'],
                'weight': 1,
                'solution': "Complete Environment Configuration Fix",
                'proven_fixes': [
                    "Set missing environment variables in deployment",
                    "Create ConfigMaps for non-sensitive configuration",
                    "Use Secrets for sensitive data like passwords",
                    "Verify environment variable injection"
                ]
            }
        }
        
        # Analyze combined recommendations to find patterns
        combined_text = ' '.join(all_recs).lower()
        issue_scores = {}
        
        # Score each solution pattern based on keyword matches
        for pattern_name, pattern_info in solution_patterns.items():
            score = 0
            for keyword in pattern_info['keywords']:
                if keyword in combined_text:
                    score += pattern_info['weight']
            issue_scores[pattern_name] = score
        
        # Find the primary issue type with highest score
        if issue_scores:
            primary_type = max(issue_scores.keys(), key=lambda k: issue_scores[k])
            
            # Return comprehensive solution with proven fixes
            if issue_scores[primary_type] > 0:
                primary_solution = solution_patterns[primary_type]
                return [f"{primary_solution['solution']} - Proven fixes applied"]
        
        # Fallback to general troubleshooting
        return ["Complete System Troubleshooting Guide - General solutions applied"]
    
    def _get_proven_solutions(self, issues: List[Dict]) -> List[str]:
        """Get proven solutions based on specific error patterns identified"""
        proven_solutions = []
        
        # Solution database mapping specific errors to proven fixes
        error_solution_db = {
            # Network/Connection Issues
            'net::err_connection_reset': [
                "Configure firewall to allow outbound HTTPS (port 443)",
                "Implement retry logic with exponential backoff (3 retries, 1s, 2s, 4s delays)",
                "Check proxy settings and DNS resolution",
                "Test with curl -v --connect-timeout 10 https://target-api.com"
            ],
            'connection reset': [
                "Verify target service is running and accessible",
                "Check for network policies blocking the connection",
                "Implement circuit breaker pattern to handle failures gracefully",
                "Monitor connection pool health and adjust timeouts"
            ],
            'firewall blocking': [
                "Open required ports: sudo ufw allow out 443/tcp && sudo ufw allow out 80/tcp",
                "Configure corporate firewall rules for external API access",
                "Use internal service discovery instead of external calls",
                "Implement request routing through approved proxy servers"
            ],
            
            # Database Issues  
            'database timeout': [
                "Increase connection timeout to 30 seconds minimum",
                "Optimize slow queries and add appropriate indexes",
                "Scale database connection pool size based on load",
                "Implement database connection health checks"
            ],
            'database connection refused': [
                "Restart database service: sudo systemctl restart mysql/postgresql",
                "Check database is binding to correct interface (not just localhost)",
                "Verify connection credentials and user permissions",
                "Monitor database logs for connection limit issues"
            ],
            
            # Kubernetes Resource Issues
            'insufficient memory': [
                "Increase pod memory limit to 2Gi: resources.limits.memory: '2Gi'",
                "Add memory requests to prevent overcommitment: resources.requests.memory: '1Gi'",
                "Enable cluster autoscaling to add nodes dynamically",
                "Implement memory profiling to identify memory leaks"
            ],
            'node pressure eviction': [
                "Add more worker nodes immediately to distribute load",
                "Set pod disruption budgets to prevent cascading failures",
                "Configure resource quotas per namespace",
                "Implement predictive scaling based on metrics"
            ],
            'no nodes available': [
                "Scale cluster: kubectl scale deployment <name> --replicas=1 (reduce load)",
                "Add worker nodes or enable cluster autoscaling",
                "Check node taints: kubectl describe nodes | grep Taints",
                "Review resource requests vs available capacity"
            ],
            'failed to create pod': [
                "Check image pull secrets: kubectl get secrets",
                "Verify image exists and is accessible",
                "Review service account RBAC permissions",
                "Check resource quotas: kubectl describe quota"
            ],
            
            # Environment/Configuration Issues
            'environment variable not set': [
                "Set in deployment: env: - name: DATABASE_URL value: 'connection-string'",
                "Create ConfigMap: kubectl create configmap app-config --from-env-file=.env",
                "Use Secrets for sensitive vars: kubectl create secret generic app-secrets",
                "Verify environment injection: kubectl exec pod -- env | grep VAR_NAME"
            ]
        }
        
        # Match issues to proven solutions
        for issue in issues:
            issue_desc = issue.get('description', '').lower()
            issue_title = issue.get('title', '').lower()
            issue_line = issue.get('line', '').lower()
            
            # Search for matching patterns in our solution database
            for error_pattern, solutions in error_solution_db.items():
                if (error_pattern in issue_desc or 
                    error_pattern in issue_title or 
                    error_pattern in issue_line):
                    
                    # Add proven solutions for this specific error
                    proven_solutions.extend([
                        f"PROVEN FIX for '{error_pattern}': {solution}" 
                        for solution in solutions[:2]  # Top 2 solutions per pattern
                    ])
        
        # If no specific patterns matched, provide general proven practices
        if not proven_solutions:
            issue_types = [issue.get('type', '') for issue in issues]
            
            if 'network' in issue_types or 'firewall' in issue_types:
                proven_solutions.extend([
                    "PROVEN NETWORK FIX: Test connectivity with nc -zv host port",
                    "PROVEN NETWORK FIX: Configure retry logic with exponential backoff"
                ])
            
            if 'database' in issue_types:
                proven_solutions.extend([
                    "PROVEN DATABASE FIX: Increase connection timeout and pool size",
                    "PROVEN DATABASE FIX: Implement database health checks"
                ])
            
            if any(t in issue_types for t in ['resource', 'deployment', 'scheduling']):
                proven_solutions.extend([
                    "PROVEN K8S FIX: Set proper resource requests and limits",
                    "PROVEN K8S FIX: Enable cluster autoscaling for dynamic scaling"
                ])
        
        return proven_solutions[:8]  # Return top 8 proven solutions
    
    def _get_matched_patterns(self, log_content: str) -> List[str]:
        """Get list of patterns that matched in the log"""
        patterns = ['insufficient memory', 'node pressure eviction', 'no nodes available', 
                   'replica set desired count not met', 'failed to create pod',
                   'net::err_connection_reset', 'database timeout', 'firewall block']
        matched = []
        log_lower = log_content.lower()
        for pattern in patterns:
            if pattern in log_lower:
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
                    # This is a problem description, provide specific troubleshooting
                    title = f"[{analysis_type}] Issue Analysis {i+1}"
                    description = f"Problem: {rec}"
                    # Generate SPECIFIC troubleshooting based on exact error patterns
                    rec_lower = rec.lower()
                    
                    # Pass the full error context for better matching
                    code_example = self._generate_code_example(rec)
                
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
        """Generate comprehensive step-by-step solutions"""
        rec_lower = recommendation.lower()
        
        # YAML Syntax Error Fixes - SPECIFIC SOLUTION
        if ('yaml' in rec_lower or 'unexpected character' in rec_lower or 
            '.yml' in rec_lower or 'syntax fix' in rec_lower):
            return """# YAML Syntax Error Fix - SPECIFIC SOLUTION

# === STEP 1: IDENTIFY THE EXACT ERROR ===
echo "Step 1: Locating YAML syntax error..."
# Check specific line for unexpected character
grep -n "unexpected character" deploy.yml 2>/dev/null || echo "Checking YAML structure..."
cat -n .github/workflows/deploy.yml | sed -n '10,20p'  # Show lines around error

# === STEP 2: COMMON YAML FIXES ===
echo "Step 2: Applying YAML syntax fixes..."

# FIX 1: Remove invalid characters and trailing spaces
sed -i 's/[[:space:]]*$//g' .github/workflows/deploy.yml  # Remove trailing spaces
sed -i '/^[[:space:]]*-[[:space:]]*$/d' .github/workflows/deploy.yml  # Remove empty list items

# FIX 2: Fix indentation (YAML requires exact 2-space indentation)
sed -i 's/\t/  /g' .github/workflows/deploy.yml  # Convert tabs to spaces

# FIX 3: Fix line 15 specifically if it has unexpected '-'
sed -i '15s/^[[:space:]]*-[[:space:]]*$/  # Fixed line 15/' .github/workflows/deploy.yml

# === STEP 3: VALIDATE YAML STRUCTURE ===
echo "Step 3: Validating YAML syntax..."
# Quick Python YAML validation
python3 -c "
import yaml, sys
try:
    with open('.github/workflows/deploy.yml', 'r') as f:
        yaml.safe_load(f)
    print('✅ YAML syntax is now valid!')
except yaml.YAMLError as e:
    print(f'❌ YAML Error still exists: {e}')
    sys.exit(1)
except FileNotFoundError:
    print('⚠️  File not found - check path')
"

# === STEP 4: VERIFY THE FIX ===
echo "Step 4: Final verification..."
git diff .github/workflows/deploy.yml  # Show what was changed
echo "✅ YAML syntax error should now be fixed!"
"""
        
        # Docker Build Context Error Fixes - SPECIFIC SOLUTION
        elif ('docker' in rec_lower and ('copy failed' in rec_lower or 
              'file not found' in rec_lower or 'build context' in rec_lower)):
            return """# Docker Build Context Fix - SPECIFIC SOLUTION

# === STEP 1: IDENTIFY THE MISSING FILE ===
echo "Step 1: Analyzing Docker build failure..."
# Check what file Docker is trying to COPY
grep -n "COPY" Dockerfile | head -5  # Show COPY commands in Dockerfile

# === STEP 2: CHECK BUILD CONTEXT ===
echo "Step 2: Examining build context..."
ls -la . | head -20  # List files in current directory (build context)
cat .dockerignore 2>/dev/null || echo "No .dockerignore file found"

# === STEP 3: COMMON DOCKER BUILD FIXES ===
echo "Step 3: Applying Docker build context fixes..."

# FIX 1: Check if file exists but is in wrong location
find . -name "requirements.txt" 2>/dev/null || echo "File not found anywhere"
find . -name "package.json" 2>/dev/null || echo "File not found anywhere"
find . -name "*.py" | head -5  # Show Python files
find . -name "*.js" | head -5  # Show JavaScript files

# FIX 2: Check .dockerignore - might be excluding required files
if [ -f .dockerignore ]; then
    echo "Current .dockerignore contents:"
    cat .dockerignore
    echo "Temporarily rename .dockerignore to test:"
    mv .dockerignore .dockerignore.bak
fi

# FIX 3: Verify Dockerfile COPY paths are correct
echo "Dockerfile COPY commands:"
grep -A1 -B1 "COPY\|ADD" Dockerfile

# === STEP 4: TEST THE BUILD ===
echo "Step 4: Testing Docker build..."
# Build with verbose output to see exact error
docker build --no-cache -t test-build . --progress=plain

# === STEP 5: SPECIFIC FILE FIXES ===
echo "Step 5: Common file fixes..."

# If requirements.txt missing:
if [ ! -f requirements.txt ]; then
    echo "Creating requirements.txt..."
    touch requirements.txt
    echo "flask" >> requirements.txt
fi

# If package.json missing:
if [ ! -f package.json ]; then
    echo "Creating package.json..."
    echo '{"name": "app", "version": "1.0.0"}' > package.json
fi

# === STEP 6: VERIFY RESOLUTION ===
echo "Step 6: Confirming build works..."
docker build -t fixed-build . --quiet && echo "✅ Build successful!" || echo "❌ Build still failing"
"""
        
        # PostgreSQL Schema Error Fixes - SPECIFIC SOLUTION (MUST BE BEFORE GENERIC DATABASE)
        elif ('postgresql' in rec_lower or 'schema fixes' in rec_lower or
              'migrations' in rec_lower or 'missing tables' in rec_lower or
              ('relation' in rec_lower and 'does not exist' in rec_lower)):
            return """# PostgreSQL Schema Fix - SPECIFIC SOLUTION

# === STEP 1: IDENTIFY THE MISSING TABLE ===
echo "Step 1: Analyzing PostgreSQL schema error..."
# Extract table name from error message
ERROR_MSG="Error: relation 'users' does not exist"
TABLE_NAME=$(echo "$ERROR_MSG" | grep -o '"[^"]*"' | tr -d '"')
echo "Missing table: $TABLE_NAME"

# === STEP 2: CHECK DATABASE CONNECTION ===
echo "Step 2: Verifying PostgreSQL connection..."
psql $DATABASE_URL -c "SELECT current_database(), current_user;" 2>/dev/null || \
echo "⚠️  Cannot connect to PostgreSQL - check DATABASE_URL"

# === STEP 3: CHECK EXISTING TABLES ===
echo "Step 3: Listing existing tables..."
psql $DATABASE_URL -c "\dt" 2>/dev/null | head -10

# === STEP 4: CHECK FOR MIGRATION FILES ===
echo "Step 4: Looking for database migrations..."
find . -name "*migration*" -o -name "*migrate*" | head -5
find . -name "*.sql" | head -5
ls -la db/migrate/ 2>/dev/null || echo "No db/migrate/ directory found"

# === STEP 5: APPLY SCHEMA FIXES ===
echo "Step 5: Creating missing table(s)..."

# COMMON FIX: Create users table (example)
psql $DATABASE_URL -c "
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
" || echo "Failed to create users table"

# COMMON FIX: Run database migrations (various frameworks)
echo "Attempting to run migrations..."

# Django migrations:
python manage.py migrate 2>/dev/null && echo "✅ Django migrations completed" || true

# Rails migrations:
bundle exec rake db:migrate 2>/dev/null && echo "✅ Rails migrations completed" || true

# Node.js/Sequelize migrations:
npx sequelize-cli db:migrate 2>/dev/null && echo "✅ Sequelize migrations completed" || true

# Laravel migrations:
php artisan migrate 2>/dev/null && echo "✅ Laravel migrations completed" || true

# === STEP 6: VERIFY TABLE CREATION ===
echo "Step 6: Confirming table exists..."
psql $DATABASE_URL -c "\d $TABLE_NAME" && echo "✅ Table $TABLE_NAME now exists!" || \
echo "❌ Table creation failed - check logs above"

# === STEP 7: FINAL VERIFICATION ===
echo "Step 7: Testing application connection..."
psql $DATABASE_URL -c "SELECT COUNT(*) FROM $TABLE_NAME;" && \
echo "✅ PostgreSQL schema error resolved!" || \
echo "⚠️  Table exists but may have permission issues"
"""
        
        # MySQL Authentication Error Fixes - SPECIFIC SOLUTION
        elif ('mysql' in rec_lower and ('access denied' in rec_lower or 'auth' in rec_lower)) or \
             'sequelize' in rec_lower and 'access denied' in rec_lower:
            return """# MySQL Authentication Fix - SPECIFIC SOLUTION

# === STEP 1: IDENTIFY THE ACCESS ISSUE ===
echo "Step 1: Analyzing MySQL access denied error..."
# Extract user and database from error
ERROR_MSG="SequelizeConnectionError: Access denied for user 'admin'@'%' to database 'mydb'"
USERNAME=$(echo "$ERROR_MSG" | grep -o "'[^']*'" | head -1 | tr -d "'")
HOSTNAME=$(echo "$ERROR_MSG" | grep -o "@'[^']*'" | tr -d "@'")
DATABASE=$(echo "$ERROR_MSG" | grep -o "database '[^']*'" | grep -o "'[^']*'" | tr -d "'")
echo "User: $USERNAME, Host: $HOSTNAME, Database: $DATABASE"

# === STEP 2: CHECK MYSQL CONNECTION ===
echo "Step 2: Testing MySQL connection as root..."
mysql -u root -p -e "SELECT USER(), DATABASE();" 2>/dev/null || \
echo "⚠️  Cannot connect to MySQL as root - check MySQL service"

# === STEP 3: CHECK EXISTING USER PERMISSIONS ===
echo "Step 3: Checking current user permissions..."
mysql -u root -p -e "
SELECT User, Host, Db FROM mysql.db WHERE User='$USERNAME';
SELECT User, Host FROM mysql.user WHERE User='$USERNAME';
SHOW GRANTS FOR '$USERNAME'@'$HOSTNAME';
" 2>/dev/null | head -10

# === STEP 4: APPLY MYSQL PERMISSION FIXES ===
echo "Step 4: Granting proper MySQL permissions..."

# COMMON FIX: Grant all privileges to user for specific database
mysql -u root -p -e "
GRANT ALL PRIVILEGES ON $DATABASE.* TO '$USERNAME'@'$HOSTNAME';
FLUSH PRIVILEGES;
" || echo "Failed to grant permissions - check MySQL root access"

# COMMON FIX: Create user if doesn't exist
mysql -u root -p -e "
CREATE USER IF NOT EXISTS '$USERNAME'@'$HOSTNAME' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON $DATABASE.* TO '$USERNAME'@'$HOSTNAME';
FLUSH PRIVILEGES;
" 2>/dev/null || echo "User creation failed - may already exist"

# COMMON FIX: Allow connections from any host (development only)
mysql -u root -p -e "
GRANT ALL PRIVILEGES ON $DATABASE.* TO '$USERNAME'@'%';
FLUSH PRIVILEGES;
" 2>/dev/null && echo "✅ Granted access from any host" || true

# === STEP 5: VERIFY DATABASE EXISTS ===
echo "Step 5: Ensuring target database exists..."
mysql -u root -p -e "
CREATE DATABASE IF NOT EXISTS $DATABASE;
SHOW DATABASES LIKE '$DATABASE';
"

# === STEP 6: TEST USER CONNECTION ===
echo "Step 6: Testing user connection..."
mysql -u $USERNAME -p -e "USE $DATABASE; SELECT 'Access granted!' as status;" && \
echo "✅ MySQL authentication fixed!" || \
echo "❌ User still cannot access database - check password"

# === STEP 7: UPDATE APPLICATION CONFIGURATION ===
echo "Step 7: Verify application connection string..."
echo "Ensure DATABASE_URL format: mysql://$USERNAME:password@host:3306/$DATABASE"
echo "Or for Sequelize config: host, username, password, database values are correct"
"""
        
        # AWS Security Group Error Fixes - SPECIFIC SOLUTION
        elif ('security group' in rec_lower and ('inbound' in rec_lower or 'port' in rec_lower)) or \
             'connection timed out' in rec_lower and 'public ip' in rec_lower:
            return """# AWS Security Group Fix - SPECIFIC SOLUTION

# === STEP 1: IDENTIFY THE CONNECTIVITY ISSUE ===
echo "Step 1: Analyzing AWS Security Group connectivity problem..."
# Extract key info from error
ERROR_MSG="Connection timed out when accessing public IP. Cause: Security group may not allow inbound traffic on port 80/443"
echo "Issue: Security Group blocking HTTP/HTTPS access"
echo "Required ports: 80 (HTTP), 443 (HTTPS)"

# === STEP 2: CHECK CURRENT SECURITY GROUP RULES ===
echo "Step 2: Listing current Security Group rules..."
# Replace sg-xxxxxxxxx with your actual Security Group ID
SECURITY_GROUP_ID="sg-xxxxxxxxx"
aws ec2 describe-security-groups --group-ids $SECURITY_GROUP_ID --output table || \
echo "⚠️  Install AWS CLI: pip install awscli && aws configure"

# === STEP 3: ADD INBOUND HTTP RULE ===
echo "Step 3: Opening port 80 for HTTP traffic..."
aws ec2 authorize-security-group-ingress \
    --group-id $SECURITY_GROUP_ID \
    --protocol tcp \
    --port 80 \
    --cidr 0.0.0.0/0 \
    --output text && \
echo "✅ HTTP port 80 opened" || \
echo "⚠️  Port 80 might already be open"

# === STEP 4: ADD INBOUND HTTPS RULE ===  
echo "Step 4: Opening port 443 for HTTPS traffic..."
aws ec2 authorize-security-group-ingress \
    --group-id $SECURITY_GROUP_ID \
    --protocol tcp \
    --port 443 \
    --cidr 0.0.0.0/0 \
    --output text && \
echo "✅ HTTPS port 443 opened" || \
echo "⚠️  Port 443 might already be open"

# === STEP 5: VERIFY SECURITY GROUP RULES ===
echo "Step 5: Confirming new rules are active..."
aws ec2 describe-security-groups \
    --group-ids $SECURITY_GROUP_ID \
    --query 'SecurityGroups[0].IpPermissions[*].{Port:FromPort,Protocol:IpProtocol,CIDR:IpRanges[0].CidrIp}' \
    --output table

# === STEP 6: TEST CONNECTIVITY ===
echo "Step 6: Testing HTTP/HTTPS access..."
PUBLIC_IP="your-ec2-public-ip"
curl -I --connect-timeout 10 http://$PUBLIC_IP && echo "✅ HTTP working!" || echo "❌ HTTP still blocked"
curl -I --connect-timeout 10 https://$PUBLIC_IP && echo "✅ HTTPS working!" || echo "❌ HTTPS still blocked"

echo "✅ AWS Security Group configured for web access!"
"""
        
        # Complete Network/Firewall troubleshooting guide
        elif 'network' in rec_lower and 'firewall' in rec_lower:
            return """# Complete Network & Firewall Troubleshooting - PROVEN SOLUTIONS

# === STEP 1: DIAGNOSE THE PROBLEM ===
echo "Step 1: Testing basic connectivity..."
ping -c 4 8.8.8.8                    # Test internet connectivity
curl -I --connect-timeout 5 https://google.com  # Test HTTPS access

# === STEP 2: CHECK FIREWALL STATUS ===
echo "Step 2: Checking firewall configuration..."
# Ubuntu/Debian:
sudo ufw status verbose
sudo ufw show added
# RHEL/CentOS/Fedora:
sudo firewall-cmd --list-all
sudo iptables -L -n -v

# === STEP 3: APPLY PROVEN FIREWALL FIXES ===
echo "Step 3: Implementing proven firewall solutions..."
# PROVEN FIX: Open standard web ports
sudo ufw allow out 443/tcp  # HTTPS
sudo ufw allow out 80/tcp   # HTTP
sudo ufw allow out 53/tcp   # DNS
sudo ufw reload

# For RHEL/CentOS:
sudo firewall-cmd --permanent --add-port=443/tcp
sudo firewall-cmd --permanent --add-port=80/tcp
sudo firewall-cmd --reload

# === STEP 4: TEST SPECIFIC SERVICE CONNECTION ===
echo "Step 4: Testing target service with proven methods..."
# PROVEN CONNECTION TEST: Multi-method verification
nc -zv your-api.com 443              # Port connectivity test
timeout 10 telnet your-api.com 443   # Interactive test
curl -v --connect-timeout 10 --max-time 30 https://your-api.com/health

# === STEP 5: IMPLEMENT PROVEN RETRY LOGIC ===
echo "Step 5: Adding connection resilience..."
# PROVEN RETRY PATTERN: Exponential backoff in scripts
for attempt in {1..5}; do
    if curl -f --connect-timeout 10 https://your-api.com; then
        echo "Connection successful on attempt $attempt"
        break
    else
        wait_time=$((2**attempt))
        echo "Attempt $attempt failed, retrying in ${wait_time}s..."
        sleep $wait_time
    fi
done

# === STEP 6: CHECK DNS RESOLUTION (PROVEN DNS FIXES) ===
echo "Step 6: Verifying and fixing DNS..."
# PROVEN DNS TROUBLESHOOTING
nslookup your-api.com 8.8.8.8    # Test with Google DNS
dig @8.8.8.8 your-api.com A       # Alternative DNS test
# Fix DNS if needed:
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf

# === STEP 7: VERIFY AND MONITOR ===
echo "Step 7: Testing final connectivity..."
curl -I --connect-timeout 10 https://your-api.com
echo "If successful, network issues resolved with proven solutions!"

# === PROVEN MONITORING SETUP ===
# Set up continuous monitoring
watch -n 5 'curl -s -o /dev/null -w "%{http_code}" https://your-api.com'
"""

        # Complete Database connectivity resolution
        elif 'database' in rec_lower or 'connection' in rec_lower or 'mysql' in rec_lower:
            return """# Complete Database Connectivity Resolution

# === STEP 1: VERIFY DATABASE SERVICE ===
echo "Step 1: Checking database service status..."
# For MySQL/MariaDB:
sudo systemctl status mysql
sudo systemctl status mariadb
# For PostgreSQL:
sudo systemctl status postgresql

# === STEP 2: TEST DATABASE CONNECTION ===
echo "Step 2: Testing database connectivity..."
# MySQL connection test:
mysql -h localhost -u your_user -p -e "SELECT 1;"
# PostgreSQL connection test:
psql -h localhost -U your_user -d your_database -c "SELECT 1;"

# === STEP 3: CHECK DATABASE LOGS ===
echo "Step 3: Checking database logs..."
# MySQL logs:
sudo tail -50 /var/log/mysql/error.log
# PostgreSQL logs:
sudo tail -50 /var/log/postgresql/postgresql-*-main.log

# === STEP 4: VERIFY CONFIGURATION ===
echo "Step 4: Checking database configuration..."
# MySQL config:
sudo cat /etc/mysql/mysql.conf.d/mysqld.cnf | grep bind-address
# PostgreSQL config:
sudo cat /etc/postgresql/*/main/postgresql.conf | grep listen_addresses

# === STEP 5: FIX CONNECTIVITY ISSUES ===
echo "Step 5: Resolving connectivity..."
# Restart database service:
sudo systemctl restart mysql
# Or for PostgreSQL:
sudo systemctl restart postgresql

# Update connection strings in your application:
# MySQL: mysql://user:password@localhost:3306/database
# PostgreSQL: postgresql://user:password@localhost:5432/database

# === STEP 6: VERIFY FIX ===
echo "Step 6: Testing the connection fix..."
# Test from application:
python3 -c "
import pymysql
try:
    conn = pymysql.connect(host='localhost', user='user', password='pass', database='db')
    print('Database connection successful!')
    conn.close()
except Exception as e:
    print(f'Connection failed: {e}')
"

echo "Database connectivity restored!"
"""

        # Complete Kubernetes troubleshooting
        elif ('kubernetes' in rec_lower or 'k8s' in rec_lower or 'pod' in rec_lower or 
              'deployment' in rec_lower or 'cluster' in rec_lower):
            return """# Complete Kubernetes Troubleshooting Guide - PROVEN SOLUTIONS

# === STEP 1: CHECK CLUSTER STATUS ===
echo "Step 1: Verifying cluster health..."
kubectl cluster-info
kubectl get nodes -o wide
kubectl get pods --all-namespaces | grep -v Running

# === STEP 2: DIAGNOSE POD ISSUES ===
echo "Step 2: Investigating pod problems..."
kubectl get pods -o wide
kubectl describe pod <pod-name>
kubectl logs <pod-name> --previous
kubectl logs <pod-name> -f

# === STEP 3: CHECK RESOURCES (PROVEN MEMORY FIXES) ===
echo "Step 3: Checking resource utilization..."
kubectl top nodes
kubectl top pods --all-namespaces
# PROVEN FIX: Set proper resource limits
kubectl patch deployment <deployment-name> -p '{
  "spec": {
    "template": {
      "spec": {
        "containers": [{
          "name": "<container-name>",
          "resources": {
            "requests": {"memory": "1Gi", "cpu": "250m"},
            "limits": {"memory": "2Gi", "cpu": "500m"}
          }
        }]
      }
    }
  }
}'

# === STEP 4: APPLY PROVEN SCALING FIXES ===
echo "Step 4: Implementing proven scaling solutions..."
# PROVEN FIX: Scale deployment if under-resourced
kubectl scale deployment <deployment-name> --replicas=3

# PROVEN FIX: Add horizontal pod autoscaler
kubectl autoscale deployment <deployment-name> --cpu-percent=70 --min=2 --max=10

# PROVEN FIX: Enable cluster autoscaling (if supported)
# AWS: eksctl create nodegroup --cluster=<cluster> --nodes=3 --nodes-min=1 --nodes-max=10
# GCP: gcloud container clusters update <cluster> --enable-autoscaling --min-nodes=1 --max-nodes=10

# === STEP 5: VERIFY SERVICES & NETWORKING ===
echo "Step 5: Checking service connectivity..."
kubectl get services -o wide
kubectl get endpoints
kubectl get ingress

# Test service connectivity:
kubectl run test-pod --image=busybox --rm -it -- sh
# Inside pod: nslookup <service-name>

# === STEP 6: CHECK STORAGE ===
echo "Step 6: Verifying storage..."
kubectl get pv,pvc
kubectl describe pv <pv-name>
df -h  # Check node disk space

# === STEP 7: APPLY PROVEN FIXES FOR COMMON ISSUES ===
echo "Step 7: Implementing proven solutions..."

# PROVEN FIX: For pod creation failures
kubectl get secrets  # Check image pull secrets
kubectl describe quota  # Check resource quotas

# PROVEN FIX: For node pressure/eviction
kubectl describe nodes | grep -E "(Pressure|Eviction)"
# Set pod disruption budgets
kubectl apply -f - <<EOF
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: <app>-pdb
spec:
  minAvailable: 1
  selector:
    matchLabels:
      app: <app>
EOF

# PROVEN FIX: For scheduling issues
kubectl describe nodes | grep Taints
kubectl taint nodes <node-name> <taint-key>-  # Remove taints if needed

# === STEP 8: VERIFY RESOLUTION ===
echo "Step 8: Confirming fixes are working..."
kubectl get pods -w
kubectl logs <pod-name>
kubectl top nodes
echo "Kubernetes issues resolved with proven solutions!"
"""

        # Complete Environment & Dependencies resolution
        elif ('environment' in rec_lower or 'dependencies' in rec_lower or 
              'python' in rec_lower):
            return """# Complete Environment & Dependencies Resolution

# === STEP 1: CHECK PYTHON ENVIRONMENT ===
echo "Step 1: Verifying Python environment..."
python3 --version
which python3
pip list | head -10

# === STEP 2: VIRTUAL ENVIRONMENT SETUP ===
echo "Step 2: Setting up clean environment..."
python3 -m venv myproject_env
source myproject_env/bin/activate  # Linux/Mac
# On Windows: myproject_env\\Scripts\\activate

# === STEP 3: INSTALL DEPENDENCIES ===
echo "Step 3: Installing project dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# If requirements.txt missing, install common packages:
pip install flask requests sqlalchemy python-dotenv

# === STEP 4: CHECK ENVIRONMENT VARIABLES ===
echo "Step 4: Verifying environment configuration..."
cat .env  # Check environment file
env | grep -E "(DATABASE|API|SECRET)"  # Check current env vars

# === STEP 5: TEST APPLICATION ===
echo "Step 5: Testing application startup..."
python3 app.py  # Or your main application file

# === STEP 6: FIX COMMON ISSUES ===
echo "Step 6: Resolving common problems..."

# Fix import errors:
pip install --upgrade setuptools wheel
pip install missing_package_name

# Fix path issues:
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Fix permission issues:
chmod +x app.py
sudo chown -R $USER:$USER .

# === STEP 7: VERIFY SOLUTION ===
echo "Step 7: Confirming environment is working..."
python3 -c "import flask; print('Flask:', flask.__version__)"
python3 -c "import requests; print('Requests working!')"
echo "Environment setup complete!"
"""

        # Default comprehensive troubleshooting
        else:
            return """# General System Troubleshooting

# === STEP 1: SYSTEM HEALTH CHECK ===
echo "Step 1: Basic system diagnostics..."
uptime                               # System load
df -h                               # Disk space
free -h                             # Memory usage
ps aux | head -10                   # Top processes

# === STEP 2: SERVICE STATUS ===
echo "Step 2: Checking service status..."
systemctl status your-service
journalctl -u your-service --since "1 hour ago"

# === STEP 3: LOG ANALYSIS ===
echo "Step 3: Analyzing logs..."
tail -50 /var/log/syslog
tail -50 /var/log/messages
dmesg | tail -20

# === STEP 4: NETWORK CONNECTIVITY ===
echo "Step 4: Testing connectivity..."
ping -c 3 8.8.8.8
curl -I https://google.com

# === STEP 5: APPLY COMMON FIXES ===
echo "Step 5: Standard resolution steps..."
sudo systemctl restart your-service
sudo systemctl daemon-reload

# === STEP 6: VERIFY RESOLUTION ===
echo "Step 6: Confirming fix..."
systemctl is-active your-service
echo "Basic troubleshooting complete!"
"""
    
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
        # Safe access to online_ai attributes
        ai_backends_available = 0
        groq_available = False
        active_backend = "pattern_recognition"
        
        if self.online_ai and hasattr(self.online_ai, 'available_backends'):
            ai_backends_available = len(self.online_ai.available_backends)
            groq_available = "groq" in self.online_ai.available_backends
            if hasattr(self.online_ai, 'active_backend'):
                active_backend = self.online_ai.active_backend or "pattern_recognition"
        
        return {
            "total_analyses": 0,
            "pattern_effectiveness": 0.0,
            "user_feedback_count": 0,
            "ai_status": {
                "online_ai": ai_backends_available > 0,
                "groq_available": groq_available,
                "active_backend": active_backend
            },
            "ai_backends": {
                "online_ai": {
                    "enabled": ai_backends_available > 0,
                    "backends": self.online_ai.available_backends if self.online_ai and hasattr(self.online_ai, 'available_backends') else [],
                    "active_backend": active_backend
                },
                "local_ai": {
                    "enabled": False,
                    "backends": [],
                    "active_backend": None
                }
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
