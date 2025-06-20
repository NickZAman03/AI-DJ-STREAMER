// DOM elements
const chatInput = document.getElementById('chatInput');
const analyzeBtn = document.getElementById('analyzeBtn');
const resultsSection = document.getElementById('resultsSection');
const moodText = document.getElementById('moodText');
const confidenceFill = document.getElementById('confidenceFill');
const confidenceText = document.getElementById('confidenceText');
const vibeText = document.getElementById('vibeText');
const genreTags = document.getElementById('genreTags');
const demoButtons = document.querySelectorAll('.demo-btn');

// New DOM elements for message player card
const messagePlayerCard = document.getElementById('messagePlayerCard');
const messageContent = document.getElementById('messageContent');
const moodEmoji = document.getElementById('moodEmoji');
const moodLabel = document.getElementById('moodLabel');
const trackTitle = document.getElementById('trackTitle');

// Live Feed DOM elements
const connectionStatus = document.getElementById('connectionStatus');
const statusText = document.getElementById('statusText');
const liveFeedContainer = document.getElementById('liveFeedContainer');

// API base URL
const API_BASE = window.location.origin;

// Mood to emoji mapping
const MOOD_EMOJIS = {
    "happy": "😊",
    "sad": "😢",
    "angry": "😠",
    "excited": "🤩",
    "neutral": "😐"
};

// List of 10 chat messages with different moods
const CHAT_MESSAGES = [
    "I'm so excited about the concert tonight! Can't wait to dance!",
    "This day has been absolutely terrible. Everything went wrong.",
    "Just finished my project and it turned out amazing!",
    "I'm feeling really down today. Nothing seems to work out.",
    "OMG! I just won the lottery! This is incredible!",
    "The weather is nice today. Pretty standard day.",
    "I'm so angry at my boss! This is completely unfair!",
    "Had a great workout this morning. Feeling energized!",
    "Lost my phone and wallet today. What a disaster.",
    "Just chilling at home, watching some TV. Pretty relaxed."
];

// Simulation variables
let simulationInterval = null;
let currentMessageIndex = 0;
let isSimulating = false;

// EventSource connection for live stream
let eventSource = null;
let reconnectAttempts = 0;
const MAX_RECONNECT_ATTEMPTS = 5;

// Initialize EventSource connection
function initializeEventSource() {
    if (eventSource) {
        eventSource.close();
    }
    
    try {
        eventSource = new EventSource(`${API_BASE}/stream`);
        
        eventSource.onopen = function(event) {
            console.log('EventSource connection opened');
            updateConnectionStatus(true, 'Connected to live stream');
            reconnectAttempts = 0;
        };
        
        eventSource.onmessage = function(event) {
            console.log('Received SSE message:', event.data);
            try {
                const data = JSON.parse(event.data);
                addFeedItem(data);
            } catch (error) {
                console.error('Error parsing SSE data:', error);
            }
        };
        
        eventSource.onerror = function(event) {
            console.error('EventSource error:', event);
            updateConnectionStatus(false, 'Connection error');
            
            if (eventSource.readyState === EventSource.CLOSED) {
                handleReconnection();
            }
        };
        
    } catch (error) {
        console.error('Error creating EventSource:', error);
        updateConnectionStatus(false, 'Failed to connect');
        handleReconnection();
    }
}

// Handle reconnection attempts
function handleReconnection() {
    if (reconnectAttempts < MAX_RECONNECT_ATTEMPTS) {
        reconnectAttempts++;
        const delay = Math.min(1000 * Math.pow(2, reconnectAttempts), 10000); // Exponential backoff, max 10s
        
        updateConnectionStatus(false, `Reconnecting... (${reconnectAttempts}/${MAX_RECONNECT_ATTEMPTS})`);
        
        setTimeout(() => {
            console.log(`Attempting to reconnect (${reconnectAttempts}/${MAX_RECONNECT_ATTEMPTS})`);
            initializeEventSource();
        }, delay);
    } else {
        updateConnectionStatus(false, 'Connection failed. Please refresh the page.');
    }
}

// Update connection status UI
function updateConnectionStatus(connected, message) {
    const statusIndicator = document.getElementById('connectionStatus');
    const statusTextElement = document.getElementById('statusText');
    const feedStatus = document.querySelector('.feed-status');
    
    if (connected) {
        statusIndicator.textContent = '🟢 Connected';
        statusIndicator.className = 'status-indicator connected';
        feedStatus.className = 'feed-status connected';
    } else {
        statusIndicator.textContent = '🔴 Disconnected';
        statusIndicator.className = 'status-indicator';
        feedStatus.className = 'feed-status';
    }
    
    statusTextElement.textContent = message;
}

// Add a new item to the live feed
function addFeedItem(data) {
    // Remove placeholder if it exists
    const placeholder = liveFeedContainer.querySelector('.feed-placeholder');
    if (placeholder) {
        placeholder.remove();
    }
    
    const feedItem = document.createElement('div');
    feedItem.className = 'feed-item';
    
    const timestamp = new Date().toLocaleTimeString();
    const mood = data.mood.toLowerCase();
    const emoji = MOOD_EMOJIS[mood] || "😊";
    
    feedItem.innerHTML = `
        <div class="feed-item-header">
            <span class="feed-timestamp">${timestamp}</span>
        </div>
        <div class="feed-message">"${data.original_message}"</div>
        <div class="feed-analysis">
            <div class="feed-mood">
                <span class="feed-mood-emoji">${emoji}</span>
                <span class="feed-mood-text">${data.mood}</span>
            </div>
            <div class="feed-track">
                <span class="feed-track-icon">🎵</span>
                <span class="feed-track-text">${data.suggested_track}</span>
            </div>
        </div>
    `;
    
    // Add to the top of the feed
    liveFeedContainer.insertBefore(feedItem, liveFeedContainer.firstChild);
    
    // Keep only the last 20 items to prevent memory issues
    const items = liveFeedContainer.querySelectorAll('.feed-item');
    if (items.length > 20) {
        items[items.length - 1].remove();
    }
    
    // Auto-scroll to the top
    liveFeedContainer.scrollTop = 0;
}

// Clean up EventSource on page unload
window.addEventListener('beforeunload', function() {
    if (eventSource) {
        eventSource.close();
    }
});

// Event listeners
analyzeBtn.addEventListener('click', analyzeMood);
chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        analyzeMood();
    }
});

// Demo button functionality
demoButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        const text = btn.getAttribute('data-text');
        chatInput.value = text;
        analyzeMood();
    });
});

// Add simulation controls
document.addEventListener('DOMContentLoaded', () => {
    addTypingAnimation();
    chatInput.focus();
    addSimulationControls();
    
    // Initialize EventSource connection for live feed
    initializeEventSource();
});

// Add simulation controls to the page
function addSimulationControls() {
    const demoSection = document.querySelector('.demo-section');
    
    const simulationDiv = document.createElement('div');
    simulationDiv.className = 'simulation-controls';
    simulationDiv.innerHTML = `
        <h3>Live Chat Simulation</h3>
        <p>Simulate 10 different chat messages being analyzed in real-time:</p>
        <div class="simulation-buttons">
            <button id="startSimulation" class="simulation-btn start-btn">🚀 Start Simulation</button>
            <button id="stopSimulation" class="simulation-btn stop-btn" style="display: none;">⏹️ Stop Simulation</button>
        </div>
        <div class="simulation-status" id="simulationStatus"></div>
    `;
    
    demoSection.appendChild(simulationDiv);
    
    // Add event listeners for simulation controls
    document.getElementById('startSimulation').addEventListener('click', startSimulation);
    document.getElementById('stopSimulation').addEventListener('click', stopSimulation);
}

// Start the simulation
function startSimulation() {
    if (isSimulating) return;
    
    isSimulating = true;
    currentMessageIndex = 0;
    
    // Update UI
    document.getElementById('startSimulation').style.display = 'none';
    document.getElementById('stopSimulation').style.display = 'inline-block';
    
    // Clear previous results
    clearSimulationResults();
    
    // Start sending messages
    sendNextMessage();
    
    // Set up interval for subsequent messages
    simulationInterval = setInterval(sendNextMessage, 2000);
}

// Stop the simulation
function stopSimulation() {
    if (!isSimulating) return;
    
    isSimulating = false;
    clearInterval(simulationInterval);
    
    // Update UI
    document.getElementById('startSimulation').style.display = 'inline-block';
    document.getElementById('stopSimulation').style.display = 'none';
    document.getElementById('simulationStatus').textContent = 'Simulation stopped.';
}

// Send the next message in the simulation
function sendNextMessage() {
    if (currentMessageIndex >= CHAT_MESSAGES.length) {
        stopSimulation();
        document.getElementById('simulationStatus').textContent = 'Simulation completed! All messages processed.';
        return;
    }
    
    const message = CHAT_MESSAGES[currentMessageIndex];
    const status = document.getElementById('simulationStatus');
    status.textContent = `Processing message ${currentMessageIndex + 1}/10: "${message.substring(0, 30)}..."`;
    
    // Simulate the API call
    simulateMoodAnalysis(message, currentMessageIndex);
    currentMessageIndex++;
}

// Simulate mood analysis for a message
async function simulateMoodAnalysis(message, index) {
    try {
        const response = await fetch(`${API_BASE}/mood`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: message
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        displaySimulationResult(message, data, index);
        
    } catch (error) {
        console.error('Error in simulation:', error);
        displaySimulationError(message, index);
    }
}

// Display simulation result
function displaySimulationResult(message, data, index) {
    const resultsContainer = document.getElementById('simulationResults') || createSimulationResultsContainer();
    
    const resultCard = document.createElement('div');
    resultCard.className = 'simulation-result-card';
    resultCard.style.animationDelay = `${index * 0.1}s`;
    
    const mood = data.mood.toLowerCase();
    const emoji = MOOD_EMOJIS[mood] || "😊";
    
    resultCard.innerHTML = `
        <div class="simulation-message">
            <span class="message-number">#${index + 1}</span>
            <span class="message-text">"${message}"</span>
        </div>
        <div class="simulation-mood">
            <span class="mood-emoji-small">${emoji}</span>
            <span class="mood-text-small">${data.mood}</span>
        </div>
        <div class="simulation-track">
            <span class="track-icon">🎵</span>
            <span class="track-text">${data.suggested_track}</span>
        </div>
    `;
    
    resultsContainer.appendChild(resultCard);
    
    // Scroll to the new result
    resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Display simulation error
function displaySimulationError(message, index) {
    const resultsContainer = document.getElementById('simulationResults') || createSimulationResultsContainer();
    
    const errorCard = document.createElement('div');
    errorCard.className = 'simulation-error-card';
    
    errorCard.innerHTML = `
        <div class="simulation-message">
            <span class="message-number">#${index + 1}</span>
            <span class="message-text">"${message}"</span>
        </div>
        <div class="error-message">❌ Analysis failed</div>
    `;
    
    resultsContainer.appendChild(errorCard);
}

// Create simulation results container
function createSimulationResultsContainer() {
    const container = document.createElement('div');
    container.id = 'simulationResults';
    container.className = 'simulation-results';
    
    const demoSection = document.querySelector('.demo-section');
    demoSection.appendChild(container);
    
    return container;
}

// Clear simulation results
function clearSimulationResults() {
    const resultsContainer = document.getElementById('simulationResults');
    if (resultsContainer) {
        resultsContainer.remove();
    }
}

// Main function to analyze mood
async function analyzeMood() {
    const text = chatInput.value.trim();
    
    if (!text) {
        showError('Please enter some text to analyze.');
        return;
    }
    
    // Show loading state
    setLoadingState(true);
    
    try {
        const response = await fetch(`${API_BASE}/analyze-mood`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: text,
                timestamp: new Date().toISOString()
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        displayResults(data);
        displayMessagePlayerCard(text, data);
        
    } catch (error) {
        console.error('Error analyzing mood:', error);
        showError('Failed to analyze mood. Please try again.');
    } finally {
        setLoadingState(false);
    }
}

// Display results
function displayResults(data) {
    // Update mood display
    moodText.textContent = data.mood;
    
    // Update confidence bar
    const confidencePercent = Math.round(data.confidence * 100);
    confidenceFill.style.width = `${confidencePercent}%`;
    confidenceText.textContent = `Confidence: ${confidencePercent}%`;
    
    // Update music vibe
    vibeText.textContent = data.music_vibe;
    
    // Update genre tags
    genreTags.innerHTML = '';
    data.suggested_genres.forEach(genre => {
        const tag = document.createElement('span');
        tag.className = 'genre-tag';
        tag.textContent = genre;
        genreTags.appendChild(tag);
    });
    
    // Show results section
    resultsSection.style.display = 'block';
    
    // Scroll to results
    resultsSection.scrollIntoView({ 
        behavior: 'smooth', 
        block: 'start' 
    });
}

// Display message player card
function displayMessagePlayerCard(originalText, data) {
    // Update original message
    messageContent.textContent = `"${originalText}"`;
    
    // Update mood emoji and label
    const mood = data.mood.toLowerCase();
    moodEmoji.textContent = MOOD_EMOJIS[mood] || "😊";
    moodLabel.textContent = data.mood;
    
    // Update track title
    trackTitle.textContent = data.suggested_track;
    
    // Show the card
    messagePlayerCard.style.display = 'grid';
    
    // Scroll to the new card
    messagePlayerCard.scrollIntoView({ 
        behavior: 'smooth', 
        block: 'start' 
    });
}

// Set loading state
function setLoadingState(loading) {
    const btnText = analyzeBtn.querySelector('.btn-text');
    const btnLoading = analyzeBtn.querySelector('.btn-loading');
    
    if (loading) {
        analyzeBtn.disabled = true;
        btnText.style.display = 'none';
        btnLoading.style.display = 'inline';
    } else {
        analyzeBtn.disabled = false;
        btnText.style.display = 'inline';
        btnLoading.style.display = 'none';
    }
}

// Show error message
function showError(message) {
    // Create a simple error notification
    const errorDiv = document.createElement('div');
    errorDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #f44336;
        color: white;
        padding: 15px 20px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 1000;
        font-weight: 500;
        max-width: 300px;
    `;
    errorDiv.textContent = message;
    
    document.body.appendChild(errorDiv);
    
    // Remove after 5 seconds
    setTimeout(() => {
        if (errorDiv.parentNode) {
            errorDiv.parentNode.removeChild(errorDiv);
        }
    }, 5000);
}

// Add some visual feedback for successful analysis
function addSuccessFeedback() {
    analyzeBtn.style.background = 'linear-gradient(135deg, #4CAF50 0%, #45a049 100%)';
    setTimeout(() => {
        analyzeBtn.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
    }, 1000);
}

// Enhanced display results with success feedback
const originalDisplayResults = displayResults;
displayResults = function(data) {
    originalDisplayResults(data);
    addSuccessFeedback();
};

// Add keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + Enter to analyze
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        analyzeMood();
    }
    
    // Escape to clear input
    if (e.key === 'Escape') {
        chatInput.value = '';
        chatInput.focus();
    }
});

// Add input character counter
chatInput.addEventListener('input', () => {
    const maxLength = 500;
    const currentLength = chatInput.value.length;
    
    if (currentLength > maxLength) {
        chatInput.value = chatInput.value.substring(0, maxLength);
    }
});

// Add some nice animations
function addTypingAnimation() {
    chatInput.style.transition = 'all 0.3s ease';
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    addTypingAnimation();
    chatInput.focus();
}); 