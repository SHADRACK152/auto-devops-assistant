"""
Mock database implementation for development
This allows us to continue building the Auto DevOps Assistant without TiDB connection
"""

import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional

class MockDatabase:
    """In-memory mock database for development"""
    
    def __init__(self):
        self.logs = {}
        self.embeddings = {}
        self.fixes = {}
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize with some sample deployment logs and fixes"""
        
        # Sample deployment logs
        sample_logs = [
            {
                'content': 'ERROR: yaml.scanner.ScannerError: mapping values are not allowed here\n  in "docker-compose.yml", line 5, column 13',
                'source': 'docker',
                'severity': 'error',
                'summary': 'YAML syntax error in docker-compose.yml'
            },
            {
                'content': 'ERROR: docker: Error response from daemon: driver failed programming external connectivity on endpoint',
                'source': 'docker',
                'severity': 'error', 
                'summary': 'Docker port binding conflict'
            },
            {
                'content': 'kubectl error: error validating "deployment.yaml": error validating data: ValidationError',
                'source': 'kubernetes',
                'severity': 'error',
                'summary': 'Kubernetes deployment validation failed'
            }
        ]
        
        # Sample error fixes
        sample_fixes = [
            {
                'error_pattern': 'yaml.scanner.ScannerError',
                'error_type': 'yaml_syntax',
                'fix_suggestion': 'Check YAML indentation and mapping syntax. Ensure proper spacing and no tabs.',
                'fix_code': 'version: "3.8"\nservices:\n  app:\n    image: nginx\n    ports:\n      - "80:80"',
                'confidence_score': 0.95
            },
            {
                'error_pattern': 'port.*already in use',
                'error_type': 'port_conflict',
                'fix_suggestion': 'Change the port number or stop the service using the port.',
                'fix_code': 'ports:\n  - "8080:80"  # Changed from 80:80',
                'confidence_score': 0.90
            }
        ]
        
        # Add sample logs
        for log_data in sample_logs:
            log_id = str(uuid.uuid4())
            self.logs[log_id] = {
                'id': log_id,
                'timestamp': datetime.now().isoformat(),
                'created_at': datetime.now().isoformat(),
                **log_data
            }
        
        # Add sample fixes
        for fix_data in sample_fixes:
            fix_id = str(uuid.uuid4())
            self.fixes[fix_id] = {
                'id': fix_id,
                'created_at': datetime.now().isoformat(),
                'usage_count': 0,
                **fix_data
            }
    
    def add_log(self, content: str, source: str = 'unknown', 
                severity: str = 'info', summary: str = '') -> str:
        """Add a new log entry"""
        log_id = str(uuid.uuid4())
        self.logs[log_id] = {
            'id': log_id,
            'content': content,
            'source': source,
            'severity': severity, 
            'summary': summary,
            'timestamp': datetime.now().isoformat(),
            'created_at': datetime.now().isoformat()
        }
        return log_id
    
    def get_log(self, log_id: str) -> Optional[Dict]:
        """Get a specific log by ID"""
        return self.logs.get(log_id)
    
    def get_all_logs(self) -> List[Dict]:
        """Get all logs"""
        return list(self.logs.values())
    
    def search_logs_by_pattern(self, pattern: str, limit: int = 5) -> List[Dict]:
        """Search logs by content pattern (simple text search)"""
        matching_logs = []
        pattern_lower = pattern.lower()
        
        for log in self.logs.values():
            if pattern_lower in log['content'].lower():
                matching_logs.append(log)
                if len(matching_logs) >= limit:
                    break
        
        return matching_logs
    
    def get_fix_suggestions(self, error_type: str = None) -> List[Dict]:
        """Get fix suggestions, optionally filtered by error type"""
        fixes = list(self.fixes.values())
        
        if error_type:
            fixes = [fix for fix in fixes if fix['error_type'] == error_type]
        
        # Sort by confidence score
        fixes.sort(key=lambda x: x['confidence_score'], reverse=True)
        return fixes
    
    def add_fix(self, error_pattern: str, error_type: str, 
                fix_suggestion: str, fix_code: str = '', 
                confidence_score: float = 0.5) -> str:
        """Add a new fix suggestion"""
        fix_id = str(uuid.uuid4())
        self.fixes[fix_id] = {
            'id': fix_id,
            'error_pattern': error_pattern,
            'error_type': error_type,
            'fix_suggestion': fix_suggestion,
            'fix_code': fix_code,
            'confidence_score': confidence_score,
            'usage_count': 0,
            'created_at': datetime.now().isoformat()
        }
        return fix_id
    
    def increment_fix_usage(self, fix_id: str):
        """Increment usage count for a fix"""
        if fix_id in self.fixes:
            self.fixes[fix_id]['usage_count'] += 1
    
    def get_stats(self) -> Dict:
        """Get database statistics"""
        return {
            'total_logs': len(self.logs),
            'total_fixes': len(self.fixes),
            'logs_by_severity': self._count_by_field('severity'),
            'logs_by_source': self._count_by_field('source'),
            'status': 'mock_database_active'
        }
    
    def _count_by_field(self, field: str) -> Dict:
        """Count logs by a specific field"""
        counts = {}
        for log in self.logs.values():
            value = log.get(field, 'unknown')
            counts[value] = counts.get(value, 0) + 1
        return counts

# Global mock database instance
mock_db = MockDatabase()

def get_mock_database():
    """Get the global mock database instance"""
    return mock_db
