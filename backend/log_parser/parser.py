"""
Log Parser Module for Auto DevOps Assistant
Handles parsing and analysis of deployment logs
"""

import re
import json
from datetime import datetime
from typing import Dict, List, Optional


class LogParser:
    """Parses deployment logs and extracts relevant information"""
    
    def __init__(self):
        self.error_patterns = {
            'yaml_error': r'yaml\.scanner\.ScannerError|yaml\.parser\.ParserError',
            'docker_error': r'docker: Error|Cannot connect to the Docker daemon',
            'k8s_error': r'error validating|kubectl.*error|pod.*failed',
            'config_missing': r'could not find file|No such file|FileNotFoundError',
            'port_error': r'port.*already in use|bind.*address already in use',
            'permission_error': r'permission denied|access denied',
            'network_error': r'connection refused|timeout|network unreachable'
        }
    
    def parse_log(self, log_content: str, source: str = 'unknown') -> Dict:
        """
        Parse log content and extract structured information
        
        Args:
            log_content (str): Raw log content
            source (str): Source of the log (docker, k8s, etc.)
            
        Returns:
            Dict: Structured log information
        """
        parsed_log = {
            'id': self._generate_log_id(),
            'content': log_content,
            'source': source,
            'timestamp': datetime.now().isoformat(),
            'errors': self._extract_errors(log_content),
            'severity': self._determine_severity(log_content),
            'summary': self._generate_summary(log_content)
        }
        
        return parsed_log
    
    def _generate_log_id(self) -> str:
        """Generate unique log ID"""
        import uuid
        return str(uuid.uuid4())
    
    def _extract_errors(self, log_content: str) -> List[Dict]:
        """Extract error patterns from log content"""
        errors = []
        
        for error_type, pattern in self.error_patterns.items():
            matches = re.finditer(pattern, log_content, re.IGNORECASE)
            for match in matches:
                errors.append({
                    'type': error_type,
                    'pattern': pattern,
                    'match': match.group(),
                    'line': self._get_line_number(log_content, match.start())
                })
        
        return errors
    
    def _determine_severity(self, log_content: str) -> str:
        """Determine log severity based on content"""
        content_lower = log_content.lower()
        
        if any(word in content_lower for word in ['error', 'failed', 'exception']):
            return 'error'
        elif any(word in content_lower for word in ['warning', 'warn']):
            return 'warning'
        elif any(word in content_lower for word in ['info', 'success']):
            return 'info'
        else:
            return 'unknown'
    
    def _generate_summary(self, log_content: str) -> str:
        """Generate brief summary of log content"""
        lines = log_content.strip().split('\n')
        if len(lines) > 5:
            return f"Log with {len(lines)} lines. First line: {lines[0][:100]}..."
        else:
            return log_content[:200] + "..." if len(log_content) > 200 else log_content
    
    def _get_line_number(self, text: str, position: int) -> int:
        """Get line number for given position in text"""
        return text[:position].count('\n') + 1
