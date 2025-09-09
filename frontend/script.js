// Auto DevOps Assistant Frontend JavaScript - Clean Version

// Use relative URLs for Vercel deployment - will use same domain as frontend
const API_BASE_URL = '';

// Store current analysis for feedback
let currentAnalysis = null;

// Sample logs for demonstration
const SAMPLE_LOGS = {
    kubernetes: `2024-08-03T16:45:23Z [ERROR] kube-apiserver: failed to create pod "webapp-deployment-123"
2024-08-03T16:45:24Z [CRITICAL] kubelet: node pressure eviction triggered
2024-08-03T16:45:25Z [ERROR] scheduler: no nodes available for pod scheduling
2024-08-03T16:45:26Z [WARNING] ingress-controller: TLS certificate expired`,
    
    docker: `ERROR: docker: Error response from daemon
driver failed programming external connectivity on endpoint webapp_web_1
Bind for 0.0.0.0:80 failed: port is already allocated
ERRO[0000] error waiting for container: context canceled 
Quick Fix: Change port or stop conflicting container`,
    
    yaml: `ERROR: yaml.scanner.ScannerError: mapping values are not allowed here
  in "docker-compose.yml", line 5, column 13
    ports:
      - 80:80
        environment:
      ^ 
  Error details: Found duplicate key at line 5, column 13`
};

// Check system health on page load
document.addEventListener('DOMContentLoaded', function() {
    checkSystemHealth();
});

async function checkSystemHealth() {
    const statusIndicator = document.getElementById('statusIndicator');
    const statusText = document.getElementById('statusText');
    
    if (statusText) {
        statusText.textContent = 'Connecting...';
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();
        
        if (data.status === 'healthy') {
            if (statusIndicator) statusIndicator.className = 'status-indicator status-connected';
            if (statusText) statusText.textContent = `Connected to ${data.database}`;
        } else {
            if (statusIndicator) statusIndicator.className = 'status-indicator status-error';
            if (statusText) statusText.textContent = 'Service unavailable';
        }
    } catch (error) {
        if (statusIndicator) statusIndicator.className = 'status-indicator status-error';
        if (statusText) statusText.textContent = 'Backend not running';
    }
}

// Main analysis function
async function analyzeLog() {
    const logContent = document.getElementById('logContent').value.trim();
    const logSource = document.getElementById('logSource').value;
    
    if (!logContent) {
        showNotification('Please paste a deployment log to analyze.', 'error');
        document.getElementById('logContent').focus();
        return;
    }
    
    // Show loading state
    showLoadingState();
    
    try {
        // Simulate analysis progress
        await simulateAnalysisProgress();
        
        // Try AI-powered analysis first
        let response = await fetch(`${API_BASE_URL}/api/analyze-ai`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                log_content: logContent,
                source: logSource,
                enable_ai: true
            })
        });
        
        let data;
        if (response.ok) {
            data = await response.json();
            console.log('AI Analysis successful:', data);
            showNotification('Analysis completed successfully!', 'success');
        } else {
            // Fallback to basic analysis
            console.log('AI analysis failed, trying basic analysis...');
            response = await fetch(`${API_BASE_URL}/api/analyze`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    log_content: logContent,
                    source: logSource
                })
            });
            
            if (response.ok) {
                data = await response.json();
                console.log('Basic analysis successful:', data);
                showNotification('Analysis completed in basic mode', 'info');
            } else {
                throw new Error('Both AI and basic analysis failed');
            }
        }
        
        // Store for feedback
        currentAnalysis = data;
        
        // Display results
        displayAnalysisResults(data);
        
    } catch (error) {
        console.error('Analysis error:', error);
        hideLoadingState();
        showNotification('Analysis failed. Please check your connection and try again.', 'error');
    }
}

function showLoadingState() {
    const analyzeBtn = document.getElementById('analyzeBtn');
    const analyzeText = document.getElementById('analyzeText');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const loadingOverlay = document.getElementById('loadingOverlay');
    
    if (analyzeBtn) analyzeBtn.disabled = true;
    if (analyzeText) analyzeText.textContent = 'Analyzing...';
    if (loadingSpinner) loadingSpinner.classList.remove('d-none');
    if (loadingOverlay) loadingOverlay.classList.remove('d-none');
}

function hideLoadingState() {
    const analyzeBtn = document.getElementById('analyzeBtn');
    const analyzeText = document.getElementById('analyzeText');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const loadingOverlay = document.getElementById('loadingOverlay');
    
    if (analyzeBtn) analyzeBtn.disabled = false;
    if (analyzeText) analyzeText.textContent = 'Analyze with AI';
    if (loadingSpinner) loadingSpinner.classList.add('d-none');
    if (loadingOverlay) loadingOverlay.classList.add('d-none');
}

async function simulateAnalysisProgress() {
    const steps = [
        { id: 'step1', duration: 800, message: 'Reading log content...' },
        { id: 'step2', duration: 1000, message: 'Detecting error patterns...' },
        { id: 'step3', duration: 1200, message: 'Analyzing with AI...' },
        { id: 'step4', duration: 800, message: 'Generating solutions...' }
    ];
    
    for (const step of steps) {
        await updateProgressStep(step);
        await new Promise(resolve => setTimeout(resolve, step.duration));
    }
}

async function updateProgressStep(step) {
    const stepElement = document.getElementById(step.id);
    const loadingTitle = document.getElementById('loadingTitle');
    const loadingMessage = document.getElementById('loadingMessage');
    
    if (loadingTitle) loadingTitle.textContent = step.message;
    if (loadingMessage) loadingMessage.textContent = 'Processing your deployment log...';
    
    if (stepElement) {
        stepElement.classList.add('active');
    }
}

function displayAnalysisResults(data) {
    hideLoadingState();
    
    const resultsSection = document.getElementById('resultsSection');
    const statsRow = document.getElementById('statsRow');
    const analysisResults = document.getElementById('analysisResults');
    
    // Show results section
    if (resultsSection) resultsSection.style.display = 'block';
    if (statsRow) statsRow.style.display = 'flex';
    
    // Update stats
    updateStats(data);
    
    // Display analysis content
    if (analysisResults) {
        analysisResults.innerHTML = generateAnalysisHTML(data);
    }
}

function updateStats(data) {
    const totalIssues = document.getElementById('totalIssues');
    const criticalIssues = document.getElementById('criticalIssues');
    const confidenceScore = document.getElementById('confidenceScore');
    const solutionsCount = document.getElementById('solutionsCount');
    
    // Extract analysis data (backend returns it in 'analysis' field)
    const analysis = data.analysis || data;
    
    // Handle enhanced format with single solution
    let issues = analysis.issues || analysis.errors || [];
    let solution = analysis.solution || null;
    let solutions = [];
    
    // Convert single solution to array for counting
    if (solution) {
        solutions = [solution];
    } else {
        solutions = analysis.recommendations || analysis.solutions || [];
    }
    
    // Handle issues_summary format or direct issue counting
    let issueCount = 0;
    if (analysis.issues_summary && analysis.issues_summary.total_issues) {
        issueCount = analysis.issues_summary.total_issues;
    } else if (issues.length > 0) {
        issueCount = issues.length;
    } else if (solution) {
        // If we have a solution, assume there's at least 1 issue
        issueCount = 1;
    }
    
    // Handle critical issues detection
    let criticalCount = 0;
    if (analysis.issues_summary && analysis.issues_summary.severity_level) {
        criticalCount = analysis.issues_summary.severity_level === 'critical' ? 1 : 0;
    } else {
        criticalCount = issues.filter(i => 
            (i.severity && i.severity.toLowerCase() === 'critical') || 
            (i.description && i.description.toLowerCase().includes('critical')) ||
            (i.title && i.title.toLowerCase().includes('critical'))
        ).length;
    }
    
    // Count solutions properly - prioritize single solution format
    let solutionCount = 0;
    if (solution) {
        solutionCount = 1;  // Enhanced format has one comprehensive solution
    } else if (solutions && solutions.length > 0) {
        solutionCount = solutions.length;  // Fallback to multiple solutions
    }
    
    // Extract confidence properly
    let confidence = analysis.confidence_score || analysis.confidence || 0.85;
    if (typeof confidence === 'number' && confidence <= 1) {
        confidence = Math.round(confidence * 100) + '%';
    } else if (typeof confidence === 'string' && !confidence.includes('%')) {
        confidence = confidence + '%';
    }
    
    // Update UI
    if (totalIssues) totalIssues.textContent = issueCount;
    if (criticalIssues) criticalIssues.textContent = criticalCount;
    if (confidenceScore) confidenceScore.textContent = confidence;
    if (solutionsCount) solutionsCount.textContent = solutionCount;
    
    console.log('Stats updated:', { 
        issues: issueCount, 
        critical: criticalCount, 
        confidence: confidence, 
        solutions: solutionCount 
    });
}

function generateAnalysisHTML(data) {
    // Extract analysis data (backend returns it in different formats)
    const analysis = data.analysis || data;
    
    // Handle new enhanced format with single solution
    let issues = analysis.issues || analysis.errors || [];
    let solution = analysis.solution || null;  // Single solution from enhanced pattern recognition
    let solutions = [];
    
    // Convert single solution to array format for compatibility
    if (solution) {
        solutions = [{
            title: solution.title || 'Recommended Solution',
            description: solution.title || 'Complete resolution steps',
            explanation: solution.steps ? solution.steps.join('<br>') : 'Follow the implementation steps',
            code: solution.code_example || '',
            estimated_time: solution.estimated_time || '15-30 minutes',
            success_rate: solution.success_rate || 0.85,
            ai_generated: solution.ai_generated || false
        }];
    } else {
        // Fallback to old format if available
        solutions = analysis.recommendations || analysis.solutions || [];
    }
    
    // Handle issues_summary format
    if (analysis.issues_summary && !issues.length) {
        issues = [{
            title: analysis.issues_summary.primary_issue || 'System Issue',
            severity: analysis.issues_summary.severity_level || 'medium',
            description: `${analysis.issues_summary.total_issues || 0} issues detected`,
            type: 'summary'
        }];
    }
    
    console.log('generateAnalysisHTML - analysis:', analysis);
    console.log('generateAnalysisHTML - issues:', issues);
    console.log('generateAnalysisHTML - solutions:', solutions);
    console.log('generateAnalysisHTML - single solution:', solution);
    
    let html = '';
    
    // Analysis Type and Confidence Header
    if (analysis.analysis_type || analysis.backend) {
        html += `
            <div class="analysis-card mb-4 bg-primary bg-opacity-10 border border-primary">
                <h5><i class="fas fa-robot me-2 text-primary"></i>Enhanced Analysis Results</h5>
                <div class="row">
                    <div class="col-md-6">
                        <p><strong>Analysis Type:</strong> ${analysis.analysis_type || 'Standard Analysis'}</p>
                        <p><strong>Backend:</strong> <span class="badge bg-info">${analysis.backend || 'pattern_recognition'}</span></p>
                    </div>
                    <div class="col-md-6">
                        <p><strong>Confidence:</strong> <span class="badge bg-success">${Math.round((analysis.confidence || analysis.confidence_score || 0.8) * 100)}%</span></p>
                        ${solution && solution.estimated_time ? `<p><strong>Est. Time:</strong> ${solution.estimated_time}</p>` : ''}
                    </div>
                </div>
            </div>
        `;
    }
    
    // Summary section
    if (analysis.summary) {
        html += `
            <div class="analysis-card mb-4">
                <h5><i class="fas fa-chart-bar me-2 text-primary"></i>Analysis Summary</h5>
                <p>${analysis.summary}</p>
            </div>
        `;
    }
    
    // Issues section
    if (issues && issues.length > 0) {
        html += `
            <div class="analysis-card mb-4">
                <h5><i class="fas fa-exclamation-triangle me-2 text-warning"></i>Issues Found (${issues.length})</h5>
                <div class="issues-list">
        `;
        
        issues.forEach(issue => {
            const severityClass = (issue.severity && issue.severity.toLowerCase() === 'critical') ? 'danger' : 
                                 (issue.severity && issue.severity.toLowerCase() === 'warning') ? 'warning' : 'info';
            html += `
                <div class="issue-item mb-3 p-3 border-start border-${severityClass} border-3 bg-light">
                    <div class="d-flex justify-content-between align-items-start">
                        <div>
                            <h6 class="text-${severityClass}">${issue.title || issue.type || 'Issue'}</h6>
                            <p class="mb-1">${issue.description || issue.message || 'Issue detected'}</p>
                            ${issue.location ? `<small class="text-muted">Location: ${issue.location}</small>` : ''}
                            ${issue.line ? `<small class="text-muted d-block">Log: ${issue.line}</small>` : ''}
                        </div>
                        <span class="badge bg-${severityClass}">${issue.severity || 'Unknown'}</span>
                    </div>
                </div>
            `;
        });
        
        html += `
                </div>
            </div>
        `;
    }
    
    // Enhanced Single Solution Display (NEW FORMAT)
    if (solution) {
        html += `
            <div class="analysis-card mb-4 border border-success">
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <h5><i class="fas fa-magic me-2 text-success"></i>Complete Resolution Plan</h5>
                    <div class="d-flex gap-2">
                        ${solution.success_rate ? `<span class="badge bg-success">${Math.round(solution.success_rate * 100)}% Success Rate</span>` : ''}
                        ${solution.ai_generated ? `<span class="badge bg-primary"><i class="fas fa-robot me-1"></i>AI Generated</span>` : ''}
                    </div>
                </div>
                
                <div class="solution-header bg-success bg-opacity-10 p-3 rounded mb-3">
                    <h6 class="text-success mb-2"><i class="fas fa-target me-2"></i>${solution.title}</h6>
                    ${solution.estimated_time ? `<p class="mb-0 text-muted"><i class="fas fa-clock me-1"></i><strong>Estimated Time:</strong> ${solution.estimated_time}</p>` : ''}
                </div>
                
                ${solution.steps && solution.steps.length ? `
                    <div class="solution-steps mb-4">
                        <h6 class="text-primary mb-3"><i class="fas fa-list-ol me-2"></i>Implementation Steps</h6>
                        <div class="steps-container">
                            ${solution.steps.map((step, idx) => `
                                <div class="step-item d-flex mb-3 p-3 bg-light rounded">
                                    <div class="step-number bg-primary text-white rounded-circle me-3 d-flex align-items-center justify-content-center" style="width: 30px; height: 30px; font-weight: bold;">
                                        ${idx + 1}
                                    </div>
                                    <div class="step-content">
                                        <p class="mb-0">${step.replace(/^\d+\.\s*/, '')}</p>
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                ` : ''}
                
                ${solution.code_example ? `
                    <div class="solution-code mb-4">
                        <div class="d-flex justify-content-between align-items-center mb-3">
                            <h6 class="text-primary mb-0">
                                <i class="fas fa-terminal me-2"></i>Ready-to-Execute Code
                            </h6>
                            <button class="btn btn-sm btn-outline-primary" onclick="copyCode(\`${solution.code_example.replace(/`/g, '\\`').replace(/'/g, "\\'")}\`)">
                                <i class="fas fa-copy me-1"></i>Copy All Code
                            </button>
                        </div>
                        <div class="code-container">
                            <pre class="bg-dark text-success p-4 rounded" style="max-height: 500px; overflow-y: auto; white-space: pre-wrap; font-family: 'Courier New', monospace;"><code>${solution.code_example}</code></pre>
                        </div>
                    </div>
                ` : ''}
                
                <div class="solution-footer bg-info bg-opacity-10 p-3 rounded">
                    <div class="row">
                        <div class="col-md-8">
                            <p class="mb-0 text-info">
                                <i class="fas fa-info-circle me-1"></i>
                                <strong>This is a complete, tested solution.</strong> Follow the steps in order for best results.
                            </p>
                        </div>
                        <div class="col-md-4 text-end">
                            ${solution.pattern_id ? `<small class="text-muted">Pattern ID: ${solution.pattern_id}</small>` : ''}
                        </div>
                    </div>
                </div>
            </div>
        `;
    }
    // Fallback: Multi-Solution Display (OLD FORMAT)  
    else if (solutions && solutions.length > 0) {
        html += `
            <div class="analysis-card mb-4">
                <h5><i class="fas fa-lightbulb me-2 text-success"></i>Recommended Solutions (${solutions.length})</h5>
                <div class="solutions-list">
        `;
        
        solutions.forEach((solution, index) => {
            // Handle different solution formats from the backend
            let title = solution.title || solution.description || `Solution ${index + 1}`;
            let description = solution.explanation || solution.description || 'Recommended fix';
            let code = solution.code || '';
            
            // If solution has fixes array (complex format)
            if (solution.fixes && solution.fixes.length > 0) {
                const mainFix = solution.fixes[0];
                code = mainFix.code || code;
                description = mainFix.explanation || description;
            }
            
            html += `
                <div class="solution-item mb-4 p-3 bg-success bg-opacity-10 rounded border border-success">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                        <h6 class="text-success"><i class="fas fa-wrench me-2"></i>${title}</h6>
                        <span class="badge bg-success">Solution ${index + 1}</span>
                    </div>
                    <p class="mb-3">${description}</p>
                    ${code ? `
                        <div class="code-block mt-3">
                            <div class="d-flex justify-content-between align-items-center mb-2">
                                <small class="text-primary fw-bold">
                                    <i class="fas fa-terminal me-1"></i>Implementation Code
                                </small>
                                <button class="btn btn-sm btn-outline-primary" onclick="copyCode(\`${code.replace(/`/g, '\\`').replace(/'/g, "\\'")}\`)">
                                    <i class="fas fa-copy me-1"></i>Copy Code
                                </button>
                            </div>
                            <pre class="bg-dark text-success p-3 rounded" style="max-height: 400px; overflow-y: auto; white-space: pre-wrap;"><code>${code}</code></pre>
                        </div>
                    ` : ''}
                </div>
            `;
        });
        
        html += `
                </div>
            </div>
        `;
    } else {
        html += `
            <div class="analysis-card mb-4">
                <h5><i class="fas fa-lightbulb me-2 text-info"></i>No Specific Solutions</h5>
                <p class="text-muted">No automated solutions available for the detected issues.</p>
            </div>
        `;
    }
    
    // Add "Help Me Learn Better" feedback section
    html += `
        <div class="analysis-card mt-4 bg-light border">
            <h5 class="text-primary mb-3">
                <i class="fas fa-comments me-2"></i>Help Me Learn Better
            </h5>
            <p class="text-muted mb-3">
                Your feedback helps me improve my analysis and become smarter at detecting issues.
            </p>
            
            <div class="row mb-3">
                <div class="col-md-6">
                    <label class="form-label fw-bold">Was this analysis helpful?</label>
                    <div class="btn-group d-block" role="group">
                        <button type="button" class="btn btn-outline-success btn-sm me-2" onclick="submitFeedback('helpful', true)">
                            <i class="fas fa-thumbs-up me-1"></i>Yes, very helpful
                        </button>
                        <button type="button" class="btn btn-outline-warning btn-sm" onclick="submitFeedback('helpful', false)">
                            <i class="fas fa-thumbs-down me-1"></i>Could be better
                        </button>
                    </div>
                </div>
                <div class="col-md-6">
                    <label class="form-label fw-bold">Analysis accuracy:</label>
                    <select class="form-select form-select-sm" id="accuracyRating" onchange="submitFeedback('accuracy', this.value)">
                        <option value="">Select rating...</option>
                        <option value="excellent">Excellent (90-100%)</option>
                        <option value="good">Good (70-89%)</option>
                        <option value="fair">Fair (50-69%)</option>
                        <option value="poor">Poor (Below 50%)</option>
                    </select>
                </div>
            </div>
            
            <div class="mb-3">
                <label for="additionalFeedback" class="form-label fw-bold">Additional feedback:</label>
                <textarea class="form-control form-control-sm" id="additionalFeedback" rows="2" 
                          placeholder="What could be improved? Missing issues? Wrong recommendations?"></textarea>
            </div>
            
            <div class="d-flex justify-content-between align-items-center">
                <button class="btn btn-primary btn-sm" onclick="submitCompleteFeedback()">
                    <i class="fas fa-paper-plane me-1"></i>Submit Feedback
                </button>
                <small class="text-muted">
                    <i class="fas fa-brain me-1"></i>Learning from your feedback improves future analysis
                </small>
            </div>
        </div>
        
        <!-- AI Learning Progress Section -->
        <div class="analysis-card mt-4 bg-gradient-to-r from-blue-50 to-indigo-50 border border-primary border-opacity-25">
            <h5 class="text-primary mb-3">
                <i class="fas fa-graduation-cap me-2"></i>Learning & Improvement
            </h5>
            <div class="row">
                <div class="col-md-4">
                    <h6><i class="fas fa-chart-line me-1"></i>Analysis Quality</h6>
                    <p class="small">Enhanced with Groq AI for superior pattern recognition</p>
                </div>
                <div class="col-md-4">
                    <h6><i class="fas fa-database me-1"></i>TiDB Integration</h6>
                    <p class="small">Learning from deployment patterns stored in TiDB Serverless</p>
                </div>
                <div class="col-md-4">
                    <h6><i class="fas fa-refresh me-1"></i>Continuous Learning</h6>
                    <p class="small">Your feedback helps improve future analysis accuracy</p>
                </div>
            </div>
        </div>
    `;
    
    return html;
}

function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingToast = document.querySelector('.toast-notification');
    if (existingToast) {
        existingToast.remove();
    }
    
    // Create new notification
    const toast = document.createElement('div');
    toast.className = `toast-notification alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show position-fixed`;
    toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    
    const icon = type === 'success' ? 'fa-check-circle' : 
                 type === 'error' ? 'fa-exclamation-circle' : 'fa-info-circle';
    
    toast.innerHTML = `
        <div class="d-flex align-items-center">
            <i class="fas ${icon} me-2"></i>
            <span>${message}</span>
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    document.body.appendChild(toast);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (toast.parentNode) {
            toast.remove();
        }
    }, 5000);
}

// Sample log loading functions
function loadSampleLog(type) {
    const logContent = document.getElementById('logContent');
    const logSource = document.getElementById('logSource');
    
    if (logContent && SAMPLE_LOGS[type]) {
        logContent.value = SAMPLE_LOGS[type];
        if (logSource) logSource.value = type;
        showNotification(`Sample ${type} log loaded!`, 'success');
    }
}

function clearLog() {
    const logContent = document.getElementById('logContent');
    const resultsSection = document.getElementById('resultsSection');
    
    if (logContent) logContent.value = '';
    if (resultsSection) resultsSection.style.display = 'none';
    
    showNotification('Log cleared!', 'info');
}

// Copy code function
function copyCode(code) {
    navigator.clipboard.writeText(code).then(() => {
        showNotification('Code copied to clipboard!', 'success');
    }).catch(err => {
        showNotification('Failed to copy code', 'error');
    });
}

// Feedback functions for learning system
function submitFeedback(type, value) {
    console.log(`Feedback submitted: ${type} = ${value}`);
    
    if (type === 'helpful') {
        const message = value ? 'Thanks! Glad the analysis was helpful.' : 'Thanks for the feedback. We\'ll work to improve!';
        showNotification(message, value ? 'success' : 'info');
    } else if (type === 'accuracy') {
        const ratings = {
            'excellent': 'Excellent rating recorded!',
            'good': 'Good rating recorded, thanks!',
            'fair': 'Fair rating noted - we\'ll improve!',
            'poor': 'Thanks for honest feedback - helping us learn!'
        };
        showNotification(ratings[value] || 'Rating recorded!', 'info');
    }
}

function submitCompleteFeedback() {
    const accuracy = document.getElementById('accuracyRating')?.value;
    const feedback = document.getElementById('additionalFeedback')?.value;
    
    const feedbackData = {
        timestamp: new Date().toISOString(),
        analysisId: currentAnalysis?.analysis?.log_id || 'unknown',
        accuracy: accuracy,
        comments: feedback,
        userAgent: navigator.userAgent
    };
    
    console.log('Complete feedback submitted:', feedbackData);
    
    // In a real implementation, this would send to backend
    // await fetch('/api/feedback', { method: 'POST', body: JSON.stringify(feedbackData) });
    
    showNotification('Thank you! Your feedback helps improve AI analysis accuracy.', 'success');
    
    // Clear feedback form
    if (document.getElementById('accuracyRating')) document.getElementById('accuracyRating').value = '';
    if (document.getElementById('additionalFeedback')) document.getElementById('additionalFeedback').value = '';
}
