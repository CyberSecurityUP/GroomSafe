// GROOMSAFE Web Interface - Application Logic

const API_BASE_URL = 'http://localhost:8090';

// State management
const state = {
    messages: [],
    currentAnalysis: null,
    apiOnline: false
};

// Initialize application
document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
    checkApiStatus();
    setInterval(checkApiStatus, 30000); // Check every 30 seconds
});

// Event Listeners
function initializeEventListeners() {
    // Example buttons
    document.querySelectorAll('.btn-example').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const example = e.currentTarget.dataset.example;
            loadExample(example);
        });
    });

    // Analyze button
    document.getElementById('analyzeBtn').addEventListener('click', analyzeConversation);

    // Message builder
    document.getElementById('addMessageBtn').addEventListener('click', addMessage);

    // Enter key in message builder
    document.getElementById('builderText').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            addMessage();
        }
    });

    // LLM provider change listener
    const llmProvider = document.getElementById('llmProvider');
    if (llmProvider) {
        llmProvider.addEventListener('change', updateLLMModels);
        // Initialize models on load
        updateLLMModels();
    }

    // LLM header click listener (in case inline onclick doesn't work)
    const llmHeader = document.querySelector('.llm-header');
    if (llmHeader) {
        console.log('LLM header found, adding click listener');
        llmHeader.addEventListener('click', function(e) {
            console.log('LLM header clicked!', e);
            toggleLLMConfig();
        });
    } else {
        console.error('LLM header not found!');
    }

    // LLM test connection button
    const testLLMBtn = document.getElementById('testLLMBtn');
    if (testLLMBtn) {
        console.log('Test LLM button found');
        testLLMBtn.addEventListener('click', testLLMConnection);
    }

    console.log('Event listeners initialized successfully');
}

// Check API Status
async function checkApiStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();

        if (response.ok) {
            updateApiStatus(true);
        } else {
            updateApiStatus(false);
        }
    } catch (error) {
        updateApiStatus(false);
    }
}

function updateApiStatus(online) {
    state.apiOnline = online;
    const statusEl = document.getElementById('apiStatus');

    if (online) {
        statusEl.classList.remove('offline');
        statusEl.querySelector('.dot').style.background = 'var(--success-color)';
    } else {
        statusEl.classList.add('offline');
        statusEl.querySelector('.dot').style.background = 'var(--danger-color)';
    }
}

// Load Example Conversation
async function loadExample(exampleType) {
    try {
        // Try to fetch from API endpoint first
        const response = await fetch(`${API_BASE_URL}/data/synthetic/${exampleType}_risk_conversation.json`);

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();

        // Populate form with example data
        document.getElementById('platformType').value = data.platform_type || 'social_media';
        document.getElementById('messageInput').value = JSON.stringify(data.messages, null, 2);

        // Update message builder
        state.messages = data.messages;
        renderMessagesList();

        console.log(`✓ Loaded ${exampleType} risk example`);
    } catch (error) {
        console.error('Error loading example:', error);
        // Fallback: generate synthetic example
        generateSyntheticExample(exampleType);
    }
}

function generateSyntheticExample(riskLevel) {
    // Generate synthetic conversation based on risk level
    const examples = {
        low: {
            platform_type: 'educational_forum',
            messages: [
                {
                    timestamp: new Date(Date.now() - 86400000).toISOString(),
                    sender_role: 'adult',
                    abstracted_text: 'Hello! I saw your question about homework. I can help with that math problem.'
                },
                {
                    timestamp: new Date(Date.now() - 82800000).toISOString(),
                    sender_role: 'minor',
                    abstracted_text: 'Thank you! I\'m stuck on problem 5.'
                },
                {
                    timestamp: new Date(Date.now() - 79200000).toISOString(),
                    sender_role: 'adult',
                    abstracted_text: 'No problem. Let me explain the steps. First, you need to...'
                },
                {
                    timestamp: new Date(Date.now() - 75600000).toISOString(),
                    sender_role: 'minor',
                    abstracted_text: 'Got it! Thanks for the help.'
                }
            ]
        },
        moderate: {
            platform_type: 'social_media',
            messages: [
                {
                    timestamp: new Date(Date.now() - 172800000).toISOString(),
                    sender_role: 'adult',
                    abstracted_text: 'Hi, I noticed you like gaming too! What games do you play?'
                },
                {
                    timestamp: new Date(Date.now() - 169200000).toISOString(),
                    sender_role: 'minor',
                    abstracted_text: 'Mostly Minecraft and Fortnite'
                },
                {
                    timestamp: new Date(Date.now() - 86400000).toISOString(),
                    sender_role: 'adult',
                    abstracted_text: 'Cool! You seem really mature for your age. Not like other kids.'
                },
                {
                    timestamp: new Date(Date.now() - 82800000).toISOString(),
                    sender_role: 'minor',
                    abstracted_text: 'Thanks I guess'
                },
                {
                    timestamp: new Date(Date.now() - 3600000).toISOString(),
                    sender_role: 'adult',
                    abstracted_text: 'Do you have Discord? We could chat more there, the connection is better.'
                }
            ]
        },
        high: {
            platform_type: 'messaging_app',
            messages: [
                {
                    timestamp: new Date(Date.now() - 259200000).toISOString(),
                    sender_role: 'adult',
                    abstracted_text: 'You can trust me, I understand you better than anyone.'
                },
                {
                    timestamp: new Date(Date.now() - 255600000).toISOString(),
                    sender_role: 'minor',
                    abstracted_text: 'My parents don\'t really get it'
                },
                {
                    timestamp: new Date(Date.now() - 172800000).toISOString(),
                    sender_role: 'adult',
                    abstracted_text: 'Exactly. That\'s why this should stay between us. They wouldn\'t understand our friendship.'
                },
                {
                    timestamp: new Date(Date.now() - 169200000).toISOString(),
                    sender_role: 'adult',
                    abstracted_text: 'Have you thought about what we discussed? About meeting up?'
                },
                {
                    timestamp: new Date(Date.now() - 86400000).toISOString(),
                    sender_role: 'minor',
                    abstracted_text: 'I don\'t know...'
                },
                {
                    timestamp: new Date(Date.now() - 7200000).toISOString(),
                    sender_role: 'adult',
                    abstracted_text: 'It\'s okay to be nervous. I felt the same way. But you\'re special.'
                }
            ]
        },
        critical: {
            platform_type: 'messaging_app',
            messages: [
                {
                    timestamp: new Date(Date.now() - 345600000).toISOString(),
                    sender_role: 'adult',
                    abstracted_text: 'Nobody understands you like I do. You\'re so mature for your age.'
                },
                {
                    timestamp: new Date(Date.now() - 259200000).toISOString(),
                    sender_role: 'adult',
                    abstracted_text: 'This is our special connection. Don\'t tell anyone, they would ruin it.'
                },
                {
                    timestamp: new Date(Date.now() - 255600000).toISOString(),
                    sender_role: 'minor',
                    abstracted_text: 'Ok I won\'t'
                },
                {
                    timestamp: new Date(Date.now() - 172800000).toISOString(),
                    sender_role: 'adult',
                    abstracted_text: 'Good. Your parents just don\'t understand. They would overreact.'
                },
                {
                    timestamp: new Date(Date.now() - 86400000).toISOString(),
                    sender_role: 'adult',
                    abstracted_text: 'I got us a private chat on Telegram. Delete these messages and add me there.'
                },
                {
                    timestamp: new Date(Date.now() - 82800000).toISOString(),
                    sender_role: 'adult',
                    abstracted_text: 'We can finally meet this weekend. Just us. I\'ll pick you up.'
                },
                {
                    timestamp: new Date(Date.now() - 3600000).toISOString(),
                    sender_role: 'adult',
                    abstracted_text: 'Are you still awake? I\'m thinking about you.'
                }
            ]
        }
    };

    const example = examples[riskLevel];
    if (example) {
        document.getElementById('platformType').value = example.platform_type;
        document.getElementById('messageInput').value = JSON.stringify(example.messages, null, 2);
        state.messages = example.messages;
        renderMessagesList();
        console.log(`✓ Generated synthetic ${riskLevel} risk example`);
    }
}

// Message Builder Functions
function addMessage() {
    const role = document.getElementById('builderRole').value;
    const text = document.getElementById('builderText').value.trim();

    if (!text) {
        showNotification('Please enter message text', 'warning');
        return;
    }

    const message = {
        timestamp: new Date().toISOString(),
        sender_role: role,
        abstracted_text: text
    };

    state.messages.push(message);
    renderMessagesList();
    updateMessageInput();

    // Clear input
    document.getElementById('builderText').value = '';
}

function removeMessage(index) {
    state.messages.splice(index, 1);
    renderMessagesList();
    updateMessageInput();
}

function renderMessagesList() {
    const listEl = document.getElementById('messagesList');

    if (state.messages.length === 0) {
        listEl.innerHTML = '<p style="text-align: center; color: #999; padding: 20px;">No messages yet</p>';
        return;
    }

    listEl.innerHTML = state.messages.map((msg, index) => `
        <div class="message-item">
            <div>
                <div class="role">${msg.sender_role}</div>
                <div class="text">${msg.abstracted_text}</div>
            </div>
            <button class="remove-btn" onclick="removeMessage(${index})">×</button>
        </div>
    `).join('');
}

function updateMessageInput() {
    document.getElementById('messageInput').value = JSON.stringify(state.messages, null, 2);
}

// Analyze Conversation
async function analyzeConversation() {
    if (!state.apiOnline) {
        showNotification('API is offline. Please check the server.', 'error');
        return;
    }

    // Get form data
    const platformType = document.getElementById('platformType').value;
    const exposureLevel = document.getElementById('exposureLevel').value;
    const analystId = document.getElementById('analystId').value;

    // Parse messages
    let messages;
    try {
        const messageInput = document.getElementById('messageInput').value;
        messages = messageInput ? JSON.parse(messageInput) : state.messages;

        if (!messages || messages.length === 0) {
            showNotification('Please add at least one message', 'warning');
            return;
        }
    } catch (error) {
        showNotification('Invalid JSON format in messages', 'error');
        return;
    }

    // Build conversation object
    const conversation = {
        messages: messages,
        start_time: messages[0].timestamp,
        end_time: messages[messages.length - 1].timestamp,
        platform_type: platformType,
        is_synthetic: true
    };

    // Build request
    const request = {
        conversation: conversation,
        exposure_level: exposureLevel
    };

    if (analystId) {
        request.analyst_id = analystId;
    }

    // Add LLM configuration if enabled
    const llmEnabled = document.getElementById('llmEnabled').checked;
    if (llmEnabled) {
        request.llm_enabled = true;
        request.llm_provider = document.getElementById('llmProvider').value;
        request.llm_model = document.getElementById('llmModel').value;

        const llmApiKey = document.getElementById('llmApiKey').value;
        if (llmApiKey) {
            request.llm_api_key = llmApiKey;
        }
    }

    // Show loading state
    showLoading();

    try {
        const response = await fetch(`${API_BASE_URL}/api/v1/assess`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(request)
        });

        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }

        const result = await response.json();
        state.currentAnalysis = result;

        // Display results
        displayResults(result);
        showNotification('Analysis completed successfully', 'success');

    } catch (error) {
        console.error('Analysis error:', error);
        showNotification(`Analysis failed: ${error.message}`, 'error');
        hideLoading();
    }
}

// Display Results
function displayResults(result) {
    hideLoading();

    const { risk_assessment, behavioral_features, humanshield_summary, explanation } = result;

    // Save to state for export functionality
    state.currentAnalysis = result;

    // Show results panel
    document.getElementById('emptyState').style.display = 'none';
    document.getElementById('resultsContent').style.display = 'block';

    // Update risk score
    updateRiskScore(risk_assessment);

    // Update behavioral features
    updateBehavioralFeatures(behavioral_features);

    // Update HUMANSHIELD summary
    updateHumanShieldSummary(humanshield_summary);

    // Update recommendations
    updateRecommendations(explanation.recommendations);

    // Update feature contributions
    updateContributions(explanation.feature_analysis.top_contributors);

    // Display LLM analysis if available
    if (risk_assessment.llm_enabled && risk_assessment.llm_analysis) {
        displayLLMAnalysis(risk_assessment.llm_analysis);
    } else {
        displayLLMAnalysis(null);
    }
}

function updateRiskScore(assessment) {
    const score = Math.round(assessment.grooming_risk_score);
    const riskLevel = assessment.risk_level;

    // Animate score
    animateScore(score);

    // Update risk level badge
    const badge = document.getElementById('riskLevelBadge');
    badge.className = `risk-level-badge ${riskLevel}`;
    document.getElementById('riskLevel').textContent = riskLevel.toUpperCase();

    // Update metrics
    document.getElementById('confidence').textContent = (assessment.confidence_level * 100).toFixed(1) + '%';
    document.getElementById('stage').textContent = formatStage(assessment.current_stage);
    document.getElementById('humanReview').textContent = assessment.requires_human_review ? '⚠️ Required' : '✓ Not Required';

    // Update progress circle color based on risk level
    const circle = document.getElementById('scoreProgressCircle');
    const colors = {
        minimal: '#28a745',
        low: '#17a2b8',
        moderate: '#ffc107',
        high: '#dc3545',
        critical: '#8b0000'
    };
    circle.style.stroke = colors[riskLevel] || '#e06228';
}

function animateScore(targetScore) {
    const scoreEl = document.getElementById('scoreValue');
    const circle = document.getElementById('scoreProgressCircle');
    const circumference = 2 * Math.PI * 90; // 2πr

    let current = 0;
    const duration = 1500;
    const startTime = performance.now();

    function animate(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);

        current = Math.round(targetScore * progress);
        scoreEl.textContent = current;

        // Update circle
        const offset = circumference - (progress * targetScore / 100 * circumference);
        circle.style.strokeDashoffset = offset;

        if (progress < 1) {
            requestAnimationFrame(animate);
        }
    }

    requestAnimationFrame(animate);
}

function updateBehavioralFeatures(features) {
    const chartEl = document.getElementById('featuresChart');

    const featureList = [
        { key: 'contact_frequency_score', label: 'Contact Frequency' },
        { key: 'persistence_after_nonresponse', label: 'Persistence After Non-Response' },
        { key: 'time_of_day_irregularity', label: 'Time Irregularity' },
        { key: 'emotional_dependency_indicators', label: 'Emotional Dependency' },
        { key: 'isolation_pressure', label: 'Isolation Pressure' },
        { key: 'secrecy_pressure', label: 'Secrecy Pressure' },
        { key: 'platform_migration_attempts', label: 'Platform Migration' },
        { key: 'tone_shift_score', label: 'Tone Shift' }
    ];

    chartEl.innerHTML = featureList.map(feature => {
        const value = features[feature.key];
        const percentage = (value * 100).toFixed(1);

        return `
            <div class="feature-bar">
                <div class="feature-label">${feature.label}</div>
                <div class="feature-progress">
                    <div class="feature-fill" style="width: ${percentage}%">
                        <span class="feature-value">${percentage}%</span>
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

function updateHumanShieldSummary(summary) {
    document.getElementById('behavioralCluster').textContent = summary.behavioral_cluster;
    document.getElementById('temporalPattern').textContent = summary.temporal_pattern_summary;

    const indicatorsEl = document.getElementById('riskIndicators');
    indicatorsEl.innerHTML = summary.key_risk_indicators.map(indicator =>
        `<li>⚠️ ${indicator}</li>`
    ).join('');
}

function updateRecommendations(recommendations) {
    const listEl = document.getElementById('recommendations');
    listEl.innerHTML = recommendations.map(rec =>
        `<li>${rec}</li>`
    ).join('');
}

function updateContributions(contributors) {
    const listEl = document.getElementById('contributions');
    listEl.innerHTML = contributors.map(contrib => `
        <div class="contribution-item">
            <div class="name">${formatFeatureName(contrib.feature)}</div>
            <div class="values">
                <span>Value: ${contrib.value.toFixed(3)}</span>
                <span>Contribution: ${contrib.contribution.toFixed(3)}</span>
            </div>
            <div class="description">${contrib.description}</div>
        </div>
    `).join('');
}

// Utility Functions
function showLoading() {
    document.getElementById('loadingState').style.display = 'block';
    document.getElementById('emptyState').style.display = 'none';
    document.getElementById('resultsContent').style.display = 'none';
}

function hideLoading() {
    document.getElementById('loadingState').style.display = 'none';
}

function formatStage(stage) {
    return stage.split('_').map(word =>
        word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
}

function formatFeatureName(name) {
    return name.split('_').map(word =>
        word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
}

function showNotification(message, type = 'info') {
    // Simple console notification for now
    // Could be enhanced with a toast notification system
    console.log(`[${type.toUpperCase()}] ${message}`);

    // You can add a toast notification library here
    alert(message);
}

// ========================================
// LLM Configuration Functions
// ========================================

// LLM Models for each provider
const LLM_MODELS = {
    'ollama': [
        { value: 'llama-guard-3', label: 'llama-guard-3 (Recommended for safety)' },
        { value: 'llama3.2', label: 'llama3.2 (General purpose)' },
        { value: 'mistral', label: 'mistral (Fast & accurate)' },
        { value: 'gemma2', label: 'gemma2 (Safety-focused)' }
    ],
    'gemini': [
        { value: 'gemini-1.5-pro', label: 'gemini-1.5-pro (Best quality)' },
        { value: 'gemini-1.5-flash', label: 'gemini-1.5-flash (Faster)' }
    ],
    'claude': [
        { value: 'claude-3-opus-20240229', label: 'Claude 3 Opus (Most capable)' },
        { value: 'claude-3-sonnet-20240229', label: 'Claude 3 Sonnet (Balanced)' },
        { value: 'claude-3-haiku-20240307', label: 'Claude 3 Haiku (Fastest)' }
    ],
    'chatgpt': [
        { value: 'gpt-4-turbo-preview', label: 'GPT-4 Turbo (Most capable)' },
        { value: 'gpt-4', label: 'GPT-4 (Reliable)' },
        { value: 'gpt-3.5-turbo', label: 'GPT-3.5 Turbo (Fast & cheap)' }
    ]
};

function toggleLLMConfig() {
    console.log('toggleLLMConfig called');
    const config = document.getElementById('llmConfig');
    const icon = document.getElementById('llmToggleIcon');

    if (!config) {
        console.error('llmConfig element not found');
        return;
    }
    if (!icon) {
        console.error('llmToggleIcon element not found');
        return;
    }

    const isHidden = config.style.display === 'none' || !config.style.display;
    console.log('Current display:', config.style.display, 'isHidden:', isHidden);

    if (isHidden) {
        config.style.display = 'block';
        icon.classList.add('open');
        console.log('LLM config opened');
    } else {
        config.style.display = 'none';
        icon.classList.remove('open');
        console.log('LLM config closed');
    }
}

function updateLLMModels() {
    const provider = document.getElementById('llmProvider').value;
    const modelSelect = document.getElementById('llmModel');
    const apiKeyGroup = document.getElementById('apiKeyGroup');
    const providerNote = document.getElementById('providerNote');

    // Clear existing options
    modelSelect.innerHTML = '';

    // Add models for selected provider
    const models = LLM_MODELS[provider] || [];
    models.forEach(model => {
        const option = document.createElement('option');
        option.value = model.value;
        option.textContent = model.label;
        modelSelect.appendChild(option);
    });

    // Show/hide API key field
    if (provider === 'ollama') {
        apiKeyGroup.style.display = 'none';
        providerNote.innerHTML = 'Requires Ollama installed: <a href="https://ollama.ai" target="_blank">ollama.ai</a>';
    } else {
        apiKeyGroup.style.display = 'block';
        providerNote.innerHTML = `Requires ${provider.toUpperCase()} API key`;
    }
}

async function testLLMConnection() {
    const provider = document.getElementById('llmProvider').value;
    const model = document.getElementById('llmModel').value;
    const statusSpan = document.getElementById('llmStatus');
    const testBtn = document.getElementById('testLLMBtn');

    // Disable button
    testBtn.disabled = true;
    testBtn.textContent = 'Testing...';

    // Clear previous status
    statusSpan.textContent = '';
    statusSpan.className = 'llm-status';

    try {
        const response = await fetch(`${API_BASE_URL}/api/v1/llm/status?provider=${provider}&model=${model}`);
        const result = await response.json();

        if (result.success && result.available) {
            statusSpan.textContent = '✓ Connected';
            statusSpan.classList.add('success');
        } else {
            statusSpan.textContent = result.message || '✗ Not available';
            statusSpan.classList.add('error');
        }
    } catch (error) {
        statusSpan.textContent = `✗ Error: ${error.message}`;
        statusSpan.classList.add('error');
    } finally {
        testBtn.disabled = false;
        testBtn.textContent = 'Test Connection';
    }
}

function displayLLMAnalysis(llmAnalysis) {
    if (!llmAnalysis) {
        document.getElementById('llmAnalysisCard').style.display = 'none';
        return;
    }

    // Show the LLM analysis card
    const card = document.getElementById('llmAnalysisCard');
    card.style.display = 'block';

    // Update provider badge
    document.getElementById('llmProviderBadge').textContent = llmAnalysis.provider.toUpperCase();

    // Update model name
    document.getElementById('llmModelName').textContent = llmAnalysis.model;

    // Update confidence
    document.getElementById('llmConfidence').textContent = `${(llmAnalysis.confidence * 100).toFixed(0)}%`;

    // Update severity badge
    const severityBadge = document.getElementById('llmSeverityBadge');
    severityBadge.textContent = llmAnalysis.severity_assessment.toUpperCase();
    severityBadge.className = `severity-badge ${llmAnalysis.severity_assessment}`;

    // Update explanation
    document.getElementById('llmExplanation').textContent = llmAnalysis.explanation || 'No detailed explanation provided.';

    // Update grooming indicators
    const indicatorsList = document.getElementById('llmGroomingIndicators');
    indicatorsList.innerHTML = '';
    if (llmAnalysis.grooming_indicators && llmAnalysis.grooming_indicators.length > 0) {
        llmAnalysis.grooming_indicators.forEach(indicator => {
            const li = document.createElement('li');
            li.textContent = indicator;
            indicatorsList.appendChild(li);
        });
    } else {
        const li = document.createElement('li');
        li.textContent = 'No specific grooming indicators detected';
        li.style.opacity = '0.5';
        indicatorsList.appendChild(li);
    }

    // Update risk factors
    const factorsList = document.getElementById('llmRiskFactors');
    factorsList.innerHTML = '';
    if (llmAnalysis.risk_factors && llmAnalysis.risk_factors.length > 0) {
        llmAnalysis.risk_factors.forEach(factor => {
            const li = document.createElement('li');
            li.textContent = factor;
            factorsList.appendChild(li);
        });
    } else {
        const li = document.createElement('li');
        li.textContent = 'No significant risk factors identified';
        li.style.opacity = '0.5';
        factorsList.appendChild(li);
    }
}

// ========================================
// Export Report Functions
// ========================================

function exportReportJSON() {
    if (!state.currentAnalysis) {
        alert('No analysis available to export. Please analyze a conversation first.');
        return;
    }

    const report = {
        generated_at: new Date().toISOString(),
        groomsafe_version: "1.0.0",
        ...state.currentAnalysis
    };

    const blob = new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'groomsafe_report_' + Date.now() + '.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    console.log('Report exported as JSON');
}

function exportReportPDF() {
    if (!state.currentAnalysis) {
        alert('No analysis available to export. Please analyze a conversation first.');
        return;
    }

    alert('PDF export will open a print dialog. Use "Save as PDF" option in your browser.');

    const report = state.currentAnalysis;
    const assessment = report.risk_assessment;

    const htmlContent = '<html><head><meta charset="UTF-8"><title>GROOMSAFE Report</title></head><body style="font-family: Arial; max-width: 800px; margin: 40px auto; padding: 20px;"><h1 style="color: #e06228; text-align: center;">GROOMSAFE Risk Assessment Report</h1><p style="text-align: center;"><strong>Generated:</strong> ' + new Date().toLocaleString() + '</p><div style="margin: 30px 0; padding: 20px; border: 2px solid #e06228; border-radius: 8px;"><h2>Risk Score: ' + Math.round(assessment.grooming_risk_score) + '/100</h2><p><strong>Risk Level:</strong> ' + assessment.risk_level.toUpperCase() + '</p><p><strong>Confidence:</strong> ' + (assessment.confidence_level * 100).toFixed(1) + '%</p><p><strong>Stage:</strong> ' + formatStage(assessment.current_stage) + '</p></div></body></html>';

    const printWindow = window.open('', '', 'width=800,height=600');
    printWindow.document.write(htmlContent);
    printWindow.document.close();
    printWindow.focus();
    setTimeout(function() {
        printWindow.print();
    }, 250);
}

// Make functions globally available
window.removeMessage = removeMessage;
window.toggleLLMConfig = toggleLLMConfig;
window.updateLLMModels = updateLLMModels;
window.testLLMConnection = testLLMConnection;
window.exportReportJSON = exportReportJSON;
window.exportReportPDF = exportReportPDF;
