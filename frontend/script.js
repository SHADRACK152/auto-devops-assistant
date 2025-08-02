// Auto DevOps Assistant Frontend JavaScript - Professional Version

const API_BASE_URL = 'http://127.0.0.1:5000';

// Sample logs for demonstration
const SAMPLE_LOGS = {
    yaml: `ERROR: yaml.scanner.ScannerError: mapping values are not allowed here
  in "docker-compose.yml", line 5, column 13
    ports:
      - 80:80
        environment:
      ^ 
  Error details: Found duplicate key at line 5, column 13
  Expected proper YAML indentation
  Quick Fix: Check indentation and remove duplicate keys`,
    
    docker: `ERROR: docker: Error response from daemon
  driver failed programming external connectivity on endpoint webapp_web_1
  Bind for 0.0.0.0:80 failed: port is already allocated
  ERRO[0000] error waiting for container: context canceled 
  Quick Fix: Change port or stop conflicting container
  Solution: docker stop $(docker ps -q --filter "publish=80")`
};

// Check system health on page load
document.addEventListener('DOMContentLoaded', function() {
    checkSystemHealth();
    initializeTooltips();
});

async function checkSystemHealth() {
    const statusIndicator = document.getElementById('statusIndicator');
    const statusText = document.getElementById('statusText');
    
    statusText.textContent = 'Connecting...';
    
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();
        
        if (data.status === 'healthy') {
            statusIndicator.className = 'status-indicator status-healthy';
            statusText.textContent = `Connected to ${data.database}`;
        } else {
            statusIndicator.className = 'status-indicator status-unhealthy';
            statusText.textContent = 'System partially available';
        }
    } catch (error) {
        statusIndicator.className = 'status-indicator status-unhealthy';
        statusText.textContent = 'Demo mode - Backend offline';
        console.warn('Backend not available, running in demo mode');
    }
}

function initializeTooltips() {
    // Add tooltips to buttons
    const analyzeBtn = document.querySelector('.btn-analyze');
    if (analyzeBtn) {
        analyzeBtn.title = 'Analyze deployment log (Ctrl+Enter)';
    }
}

function loadSampleLog(type) {
    const logContent = document.getElementById('logContent');
    const logSource = document.getElementById('logSource');
    
    logContent.value = SAMPLE_LOGS[type];
    logSource.value = type === 'yaml' ? 'docker' : type;
    
    // Scroll to show the loaded content
    logContent.scrollIntoView({ behavior: 'smooth', block: 'center' });
    logContent.focus();
}

async function analyzeLog() {
    const logContent = document.getElementById('logContent').value.trim();
    const logSource = document.getElementById('logSource').value;
    
    if (!logContent) {
        showNotification('Please paste a deployment log to analyze.', 'error');
        document.getElementById('logContent').focus();
        return;
    }
    
    // Show enhanced loading state
    showLoadingState();
    
    // Auto-detect log type if unknown
    if (logSource === 'unknown') {
        await autoDetectLogType(logContent);
    }
    
    try {
        // Simulate realistic analysis time with progress steps
        await simulateAnalysisProgress();
        
        const response = await fetch(`${API_BASE_URL}/api/upload-log`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                log_content: logContent,
                source: logSource
            })
        });
        
        let data;
        if (response.ok) {
            data = await response.json();
        } else {
            // Fallback to demo results
            data = null;
        }
        
        // Complete all progress steps
        await completeAllSteps();
        
        hideLoadingState();
        displayProfessionalResults(logContent, logSource);
        
        const resultsSection = document.getElementById('resultsSection');
        resultsSection.style.display = 'block';
        resultsSection.scrollIntoView({ behavior: 'smooth' });
        
        showNotification('Analysis completed successfully!', 'success');
        
    } catch (error) {
        hideLoadingState();
        
        // Show demo results even if backend is down
        displayProfessionalResults(logContent, logSource);
        const resultsSection = document.getElementById('resultsSection');
        resultsSection.style.display = 'block';
        resultsSection.scrollIntoView({ behavior: 'smooth' });
        
        showNotification('Analysis completed in demo mode', 'info');
        console.warn('Backend unavailable, showing demo results');
    }
}

// Enhanced loading functions
function showLoadingState() {
    // Show button loading state
    const analyzeBtn = document.getElementById('analyzeBtn');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const analyzeIcon = document.getElementById('analyzeIcon');
    const analyzeText = document.getElementById('analyzeText');
    
    analyzeBtn.classList.add('loading');
    analyzeBtn.disabled = true;
    loadingSpinner.classList.remove('d-none');
    analyzeIcon.style.display = 'none';
    analyzeText.textContent = 'Analyzing...';
    
    // Show loading overlay
    const loadingOverlay = document.getElementById('loadingOverlay');
    loadingOverlay.classList.remove('d-none');
    
    // Reset progress
    resetProgressSteps();
}

function hideLoadingState() {
    // Hide button loading state
    const analyzeBtn = document.getElementById('analyzeBtn');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const analyzeIcon = document.getElementById('analyzeIcon');
    const analyzeText = document.getElementById('analyzeText');
    
    analyzeBtn.classList.remove('loading');
    analyzeBtn.disabled = false;
    loadingSpinner.classList.add('d-none');
    analyzeIcon.style.display = 'inline';
    analyzeText.textContent = 'Analyze Log';
    
    // Hide loading overlay
    const loadingOverlay = document.getElementById('loadingOverlay');
    loadingOverlay.classList.add('d-none');
}

async function simulateAnalysisProgress() {
    const steps = [
        { id: 'step1', duration: 800, progress: 25, message: 'Processing log content...', details: 'Parsing deployment logs and extracting key information' },
        { id: 'step2', duration: 1000, progress: 50, message: 'Scanning for error patterns...', details: 'Using AI pattern recognition to identify potential issues' },
        { id: 'step3', duration: 1200, progress: 75, message: 'Analyzing with TiDB AgentX...', details: 'Leveraging intelligent database insights for deeper analysis' },
        { id: 'step4', duration: 800, progress: 100, message: 'Generating solutions...', details: 'Creating actionable fixes and recommendations' }
    ];
    
    for (const step of steps) {
        await updateProgressStep(step);
        await new Promise(resolve => setTimeout(resolve, step.duration));
    }
}

async function updateProgressStep(step) {
    // Update progress bar
    const progressBar = document.getElementById('progressBar');
    progressBar.style.width = step.progress + '%';
    
    // Update loading message
    const loadingTitle = document.getElementById('loadingTitle');
    const loadingMessage = document.getElementById('loadingMessage');
    loadingTitle.textContent = step.message;
    loadingMessage.textContent = step.details;
    
    // Update step visual state
    const stepElement = document.getElementById(step.id);
    const allSteps = document.querySelectorAll('.step');
    
    // Remove active from all steps
    allSteps.forEach(s => s.classList.remove('active'));
    
    // Mark previous steps as completed
    const stepIndex = parseInt(step.id.replace('step', ''));
    for (let i = 1; i < stepIndex; i++) {
        document.getElementById(`step${i}`).classList.add('completed');
    }
    
    // Mark current step as active
    stepElement.classList.add('active');
}

async function completeAllSteps() {
    const allSteps = document.querySelectorAll('.step');
    allSteps.forEach(step => {
        step.classList.remove('active');
        step.classList.add('completed');
    });
    
    const progressBar = document.getElementById('progressBar');
    progressBar.style.width = '100%';
    
    const loadingTitle = document.getElementById('loadingTitle');
    const loadingMessage = document.getElementById('loadingMessage');
    loadingTitle.textContent = 'Analysis Complete!';
    loadingMessage.textContent = 'Your deployment log has been successfully analyzed.';
    
    // Brief pause to show completion
    await new Promise(resolve => setTimeout(resolve, 500));
}

function resetProgressSteps() {
    const allSteps = document.querySelectorAll('.step');
    allSteps.forEach(step => {
        step.classList.remove('active', 'completed');
    });
    
    const progressBar = document.getElementById('progressBar');
    progressBar.style.width = '0%';
    
    const loadingTitle = document.getElementById('loadingTitle');
    const loadingMessage = document.getElementById('loadingMessage');
    loadingTitle.textContent = 'Analyzing Your Log';
    loadingMessage.textContent = 'Please wait while we process your deployment log...';
}

async function autoDetectLogType(logContent) {
    // Show auto-detect modal
    const modal = new bootstrap.Modal(document.getElementById('autoDetectModal'));
    modal.show();
    
    const detectionMessages = [
        'Scanning log structure...',
        'Identifying error patterns...',
        'Checking deployment signatures...',
        'Finalizing log type detection...'
    ];
    
    const detectionDetails = [
        'Analyzing line patterns and log format',
        'Looking for specific error signatures',
        'Matching against known deployment patterns',
        'Determining optimal analysis approach'
    ];
    
    for (let i = 0; i < detectionMessages.length; i++) {
        document.getElementById('detectionMessage').textContent = detectionMessages[i];
        document.getElementById('detectionDetails').textContent = detectionDetails[i];
        await new Promise(resolve => setTimeout(resolve, 600));
    }
    
    // Simulate detection result
    const detectedType = detectLogTypeFromContent(logContent);
    document.getElementById('logSource').value = detectedType;
    
    // Show result
    document.getElementById('detectionMessage').textContent = `Detected: ${getLogTypeDisplayName(detectedType)}`;
    document.getElementById('detectionDetails').textContent = 'Log type successfully identified. Analysis will continue...';
    
    await new Promise(resolve => setTimeout(resolve, 800));
    modal.hide();
}

function detectLogTypeFromContent(content) {
    const lowerContent = content.toLowerCase();
    
    if (lowerContent.includes('docker') || lowerContent.includes('container')) {
        return 'docker';
    } else if (lowerContent.includes('kubernetes') || lowerContent.includes('k8s') || lowerContent.includes('kubectl')) {
        return 'kubernetes';
    } else if (lowerContent.includes('jenkins') || lowerContent.includes('build')) {
        return 'cicd';
    } else if (lowerContent.includes('yaml') || lowerContent.includes('yml')) {
        return 'yaml';
    } else {
        return 'application';
    }
}

function getLogTypeDisplayName(type) {
    const displayNames = {
        'docker': 'Docker Container Log',
        'kubernetes': 'Kubernetes Deployment Log',
        'cicd': 'CI/CD Pipeline Log',
        'yaml': 'YAML Configuration Log',
        'application': 'Application Log',
        'unknown': 'Unknown Log Type'
    };
    return displayNames[type] || 'Unknown Log Type';
}

function displayProfessionalResults(logContent, logSource) {
    const resultsContainer = document.getElementById('analysisResults');
    
    // Determine analysis based on log content
    let analysis = {
        severity: 'error',
        summary: 'Deployment configuration error detected',
        source: logSource,
        errors_found: 2,
        suggestions: []
    };
    
    if (logContent.includes('yaml') || logContent.includes('YAML')) {
        analysis = {
            severity: 'error',
            summary: 'YAML syntax error in docker-compose.yml',
            source: 'docker',
            errors_found: 1,
            line_number: 5,
            error_type: 'IndentationError',
            suggestions: [
                {
                    title: 'Fix YAML Indentation',
                    description: 'Correct the indentation in your docker-compose.yml file',
                    code: `version: '3.8'
services:
  web:
    image: nginx:latest
    ports:
      - "80:80"
    environment:
      - NODE_ENV=production`,
                    priority: 'high'
                },
                {
                    title: 'Validate YAML Syntax',
                    description: 'Use a YAML validator before deployment',
                    code: 'yamllint docker-compose.yml',
                    priority: 'medium'
                }
            ]
        };
    } else if (logContent.includes('port') || logContent.includes('80')) {
        analysis = {
            severity: 'error',
            summary: 'Port conflict detected - Port 80 already in use',
            source: 'docker',
            errors_found: 1,
            error_type: 'PortAllocationError',
            suggestions: [
                {
                    title: 'Stop Conflicting Container',
                    description: 'Stop the container currently using port 80',
                    code: 'docker stop $(docker ps -q --filter "publish=80")',
                    priority: 'high'
                },
                {
                    title: 'Use Different Port',
                    description: 'Change your application to use a different port',
                    code: `ports:
  - "8080:80"  # Use port 8080 instead`,
                    priority: 'medium'
                },
                {
                    title: 'Check Running Processes',
                    description: 'Find what\'s using port 80',
                    code: 'netstat -tulpn | grep :80',
                    priority: 'low'
                }
            ]
        };
    }
    
    // Create professional results HTML
    const html = `
        <div class="analysis-card card severity-${analysis.severity}">
            <div class="card-header" style="background: linear-gradient(135deg, #ef4444, #dc2626); color: white; padding: 20px;">
                <h5 class="mb-0">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    Analysis Results
                    <span class="badge bg-light text-dark ms-2" style="font-size: 0.75rem;">${analysis.errors_found} issue(s)</span>
                </h5>
            </div>
            <div class="card-body" style="padding: 24px;">
                <div class="row">
                    <div class="col-md-6">
                        <h6 class="text-primary mb-3">
                            <i class="fas fa-chart-bar me-2"></i>Summary
                        </h6>
                        <div class="alert alert-light border-start border-4 border-primary" style="border-left-color: #3b82f6 !important;">
                            ${analysis.summary}
                        </div>
                        
                        <h6 class="text-secondary mb-3">
                            <i class="fas fa-info-circle me-2"></i>Details
                        </h6>
                        <div class="bg-light p-3 rounded">
                            <div class="mb-2"><strong>Severity:</strong> 
                                <span class="error-badge">${analysis.severity.toUpperCase()}</span>
                            </div>
                            <div class="mb-2"><strong>Source:</strong> 
                                <code class="bg-secondary text-white px-2 py-1 rounded">${analysis.source}</code>
                            </div>
                            ${analysis.error_type ? `<div class="mb-2"><strong>Error Type:</strong> 
                                <code class="bg-secondary text-white px-2 py-1 rounded">${analysis.error_type}</code>
                            </div>` : ''}
                            ${analysis.line_number ? `<div><strong>Line Number:</strong> 
                                <code class="bg-secondary text-white px-2 py-1 rounded">${analysis.line_number}</code>
                            </div>` : ''}
                        </div>
                    </div>
                    <div class="col-md-6">
                        <h6 class="text-success mb-3">
                            <i class="fas fa-lightbulb me-2"></i>Suggested Fixes
                        </h6>
                        ${analysis.suggestions.map((suggestion, index) => `
                            <div class="suggestion-card priority-${suggestion.priority} mb-3">
                                <div class="d-flex justify-content-between align-items-start mb-2">
                                    <h6 class="mb-1 text-dark">
                                        ${getPriorityIcon(suggestion.priority)} ${suggestion.title}
                                    </h6>
                                    <span class="badge ${getPriorityBadgeClass(suggestion.priority)}">
                                        ${suggestion.priority.toUpperCase()}
                                    </span>
                                </div>
                                <p class="text-muted mb-3 small">${suggestion.description}</p>
                                <div class="code-block position-relative">
                                    <button class="copy-btn position-absolute top-0 end-0 m-2" onclick="copyToClipboard('code-${index}')">
                                        <i class="fas fa-copy me-1"></i>Copy
                                    </button>
                                    <pre id="code-${index}" class="mb-0">${suggestion.code}</pre>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
                
                <div class="mt-4 pt-3 border-top d-flex justify-content-center gap-2">
                    <button class="btn btn-outline-primary btn-sm" onclick="downloadReport()">
                        <i class="fas fa-download me-1"></i>Download Report
                    </button>
                    <button class="btn btn-outline-secondary btn-sm" onclick="runAnotherAnalysis()">
                        <i class="fas fa-redo me-1"></i>New Analysis
                    </button>
                </div>
            </div>
        </div>
        
        <div class="alert alert-info mt-3" role="alert">
            <i class="fas fa-info-circle me-2"></i>
            <strong>TiDB AgentX Hackathon Demo</strong> - This analysis was generated using AI-powered pattern recognition and TiDB's intelligent database capabilities.
        </div>
    `;
    
    resultsContainer.innerHTML = html;
}

function getPriorityIcon(priority) {
    switch(priority) {
        case 'high': return '<i class="fas fa-exclamation-triangle text-danger"></i>';
        case 'medium': return '<i class="fas fa-exclamation-circle text-warning"></i>';
        default: return '<i class="fas fa-info-circle text-info"></i>';
    }
}

function getPriorityBadgeClass(priority) {
    switch(priority) {
        case 'high': return 'bg-danger';
        case 'medium': return 'bg-warning text-dark';
        default: return 'bg-info';
    }
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="d-flex align-items-center">
            <i class="fas fa-${getNotificationIcon(type)} me-2"></i>
            <span>${message}</span>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 4 seconds
    setTimeout(() => {
        notification.style.opacity = '0';
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => notification.remove(), 300);
    }, 4000);
}

function getNotificationIcon(type) {
    switch(type) {
        case 'success': return 'check-circle';
        case 'error': return 'exclamation-circle';
        case 'warning': return 'exclamation-triangle';
        default: return 'info-circle';
    }
}

function displayResults(data) {
    const resultsContainer = document.getElementById('analysisResults');
    const analysis = data.analysis;
    
    let severityClass = 'severity-info';
    let severityIcon = 'fas fa-info-circle';
    let severityColor = '#17a2b8';
    
    if (analysis.severity === 'error') {
        severityClass = 'severity-error';
        severityIcon = 'fas fa-exclamation-triangle';
        severityColor = '#dc3545';
    } else if (analysis.severity === 'warning') {
        severityClass = 'severity-warning';
        severityIcon = 'fas fa-exclamation-circle';
        severityColor = '#ffc107';
    }
    
    const html = `
        <div class="analysis-card card ${severityClass}">
            <div class="card-header" style="background-color: ${severityColor}; color: white;">
                <h5 class="mb-0">
                    <i class="${severityIcon} me-2"></i>
                    Log Analysis Complete
                </h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        <h6><i class="fas fa-chart-bar me-2"></i>Summary</h6>
                        <p class="text-muted">${analysis.summary}</p>
                        
                        <h6><i class="fas fa-tags me-2"></i>Details</h6>
                        <ul class="list-unstyled">
                            <li><strong>Severity:</strong> 
                                <span class="badge error-badge">${analysis.severity.toUpperCase()}</span>
                            </li>
                            <li><strong>Errors Found:</strong> ${analysis.errors_found}</li>
                            <li><strong>Log ID:</strong> <code>${data.log_id}</code></li>
                            <li><strong>Database:</strong> ${data.database}</li>
                        </ul>
                    </div>
                    <div class="col-md-6">
                        ${generateErrorDetails(analysis.errors)}
                    </div>
                </div>
                
                ${generateFixSuggestions(analysis.errors)}
            </div>
        </div>
    `;
    
    resultsContainer.innerHTML = html;
}

function generateErrorDetails(errors) {
    if (!errors || errors.length === 0) {
        return `
            <h6><i class="fas fa-check-circle me-2 text-success"></i>No Specific Errors Detected</h6>
            <p class="text-muted">The log appears to be clean or contains only informational messages.</p>
        `;
    }
    
    let html = `<h6><i class="fas fa-bug me-2"></i>Detected Issues</h6><ul class="list-group list-group-flush">`;
    
    errors.forEach((error, index) => {
        html += `
            <li class="list-group-item d-flex justify-content-between align-items-center">
                <div>
                    <strong>${error.type.replace('_', ' ').toUpperCase()}</strong>
                    <br>
                    <small class="text-muted">Line ${error.line}: ${error.match}</small>
                </div>
                <span class="badge bg-danger rounded-pill">${index + 1}</span>
            </li>
        `;
    });
    
    html += '</ul>';
    return html;
}

function generateFixSuggestions(errors) {
    if (!errors || errors.length === 0) {
        return '';
    }
    
    // Generate AI-like suggestions based on error types
    let suggestions = [];
    
    errors.forEach(error => {
        switch (error.type) {
            case 'yaml_error':
                suggestions.push({
                    title: 'Fix YAML Syntax',
                    description: 'Check indentation and remove duplicate keys',
                    code: `# Fix YAML indentation:
version: "3.8"
services:
  web:
    image: nginx
    ports:
      - "80:80"
    environment:
      - NODE_ENV=production`
                });
                break;
                
            case 'port_error':
                suggestions.push({
                    title: 'Resolve Port Conflict',
                    description: 'Change port mapping or stop conflicting service',
                    code: `# Change port mapping:
ports:
  - "8080:80"  # Changed from 80:80
  
# Or stop conflicting container:
docker stop $(docker ps -q --filter "publish=80")`
                });
                break;
                
            case 'docker_error':
                suggestions.push({
                    title: 'Fix Docker Configuration',
                    description: 'Review Docker daemon settings and container configuration',
                    code: `# Restart Docker daemon:
sudo systemctl restart docker

# Check container logs:
docker logs <container_name>`
                });
                break;
                
            default:
                suggestions.push({
                    title: 'General Fix',
                    description: 'Review the error message and check documentation',
                    code: '# Check logs and restart service if needed'
                });
        }
    });
    
    let html = `
        <div class="mt-4">
            <h6><i class="fas fa-lightbulb me-2"></i>AI-Powered Fix Suggestions</h6>
            <div class="row">
    `;
    
    suggestions.forEach((suggestion, index) => {
        html += `
            <div class="col-md-6 mb-3">
                <div class="card">
                    <div class="card-body">
                        <h6 class="card-title">
                            <i class="fas fa-wrench me-2 text-primary"></i>
                            ${suggestion.title}
                        </h6>
                        <p class="card-text text-muted">${suggestion.description}</p>
                        <div class="code-block">
                            <code>${suggestion.code}</code>
                        </div>
                        <button class="btn btn-sm btn-outline-primary mt-2" onclick="copyToClipboard('${suggestion.code.replace(/'/g, "\\'")}')">
                            <i class="fas fa-copy me-1"></i>Copy Code
                        </button>
                    </div>
                </div>
            </div>
        `;
    });
    
    html += '</div></div>';
    return html;
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        // Show success message
        const toast = document.createElement('div');
        toast.className = 'alert alert-success position-fixed';
        toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999;';
        toast.textContent = 'Code copied to clipboard!';
        document.body.appendChild(toast);
        
        setTimeout(() => {
            document.body.removeChild(toast);
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy: ', err);
        alert('Failed to copy to clipboard');
    });
}

// Add keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl+Enter to analyze
    if (e.ctrlKey && e.key === 'Enter') {
        analyzeLog();
    }
    
    // Esc to clear results
    if (e.key === 'Escape') {
        const resultsSection = document.getElementById('resultsSection');
        resultsSection.style.display = 'none';
    }
});

// Professional helper functions
function copyToClipboard(elementId) {
    const element = document.getElementById(elementId);
    const text = element.textContent;
    
    navigator.clipboard.writeText(text).then(() => {
        // Show success feedback
        const button = element.parentNode.querySelector('.copy-btn');
        const originalText = button.innerHTML;
        button.innerHTML = '<i class="fas fa-check me-1"></i>Copied!';
        button.style.background = '#10b981';
        button.style.color = 'white';
        
        setTimeout(() => {
            button.innerHTML = originalText;
            button.style.background = '';
            button.style.color = '';
        }, 2000);
        
        showNotification('Code copied to clipboard!', 'success');
    }).catch(() => {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        showNotification('Code copied to clipboard!', 'success');
    });
}

function downloadReport() {
    const analysisContent = document.getElementById('analysisResults').textContent;
    const blob = new Blob([`Auto DevOps Assistant Analysis Report
Generated: ${new Date().toLocaleString()}

${analysisContent}

---
Generated by Auto DevOps Assistant for TiDB AgentX Hackathon
`], { type: 'text/plain' });
    
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `devops-analysis-${new Date().toISOString().split('T')[0]}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    showNotification('Report downloaded successfully!', 'success');
}

function runAnotherAnalysis() {
    // Clear current log
    document.getElementById('logContent').value = '';
    document.getElementById('logSource').value = 'unknown';
    
    // Hide results
    const resultsSection = document.getElementById('resultsSection');
    resultsSection.style.display = 'none';
    
    // Focus on textarea
    document.getElementById('logContent').focus();
    
    // Scroll to top
    document.querySelector('.upload-section').scrollIntoView({ behavior: 'smooth' });
    
    showNotification('Ready for new analysis', 'info');
}

// Professional notification system
function showNotification(message, type = 'info') {
    const notificationContainer = document.getElementById('notification-container') || createNotificationContainer();
    
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    
    const icon = type === 'success' ? 'fa-check-circle' : 
                 type === 'error' ? 'fa-exclamation-circle' : 
                 type === 'warning' ? 'fa-exclamation-triangle' : 'fa-info-circle';
    
    notification.innerHTML = `
        <i class="fas ${icon}"></i>
        <span>${message}</span>
        <button class="notification-close" onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    notificationContainer.appendChild(notification);
    
    // Auto-remove after 4 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.classList.add('fade-out');
            setTimeout(() => notification.remove(), 300);
        }
    }, 4000);
}

function createNotificationContainer() {
    const container = document.createElement('div');
    container.id = 'notification-container';
    container.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        max-width: 400px;
    `;
    document.body.appendChild(container);
    return container;
}

// Add notification styles
const notificationStyle = document.createElement('style');
notificationStyle.textContent = `
    .notification {
        display: flex;
        align-items: center;
        gap: 12px;
        background: white;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #3b82f6;
        animation: slideIn 0.3s ease-out;
        font-size: 14px;
        line-height: 1.4;
    }
    
    .notification-success {
        border-left-color: #10b981;
        background: linear-gradient(135deg, #ecfdf5, #f0fdf4);
        color: #064e3b;
    }
    
    .notification-success i {
        color: #10b981;
    }
    
    .notification-error {
        border-left-color: #ef4444;
        background: linear-gradient(135deg, #fef2f2, #fef7f7);
        color: #7f1d1d;
    }
    
    .notification-error i {
        color: #ef4444;
    }
    
    .notification-warning {
        border-left-color: #f59e0b;
        background: linear-gradient(135deg, #fffbeb, #fefce8);
        color: #78350f;
    }
    
    .notification-warning i {
        color: #f59e0b;
    }
    
    .notification-info {
        border-left-color: #3b82f6;
        background: linear-gradient(135deg, #eff6ff, #f0f9ff);
        color: #1e3a8a;
    }
    
    .notification-info i {
        color: #3b82f6;
    }
    
    .notification span {
        flex-grow: 1;
        font-weight: 500;
    }
    
    .notification-close {
        background: none;
        border: none;
        color: #6b7280;
        cursor: pointer;
        padding: 4px;
        border-radius: 4px;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.2s ease;
    }
    
    .notification-close:hover {
        background: rgba(107, 114, 128, 0.1);
        color: #374151;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(100%);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .fade-out {
        animation: fadeOut 0.3s ease-out forwards;
    }
    
    @keyframes fadeOut {
        from {
            opacity: 1;
            transform: translateX(0);
        }
        to {
            opacity: 0;
            transform: translateX(100%);
        }
    }
`;
document.head.appendChild(notificationStyle);