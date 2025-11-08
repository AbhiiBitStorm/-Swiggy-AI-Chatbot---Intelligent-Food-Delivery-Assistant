// Update sendMessage function
async function sendMessage() {
    const input = document.getElementById('messageInput');
    const message = input.value.trim();
    
    if (!message || isTyping) return;
    
    input.value = '';
    addMessage(message, 'user');
    showTypingIndicator();
    
    const startTime = Date.now();
    
    try {
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                session_id: sessionId
            })
        });
        
        const data = await response.json();
        const responseTime = ((Date.now() - startTime) / 1000).toFixed(2);
        
        hideTypingIndicator();
        
        // Add response with timing
        addMessage(data.response, 'bot', responseTime);
        
    } catch (error) {
        console.error('Error:', error);
        hideTypingIndicator();
        addMessage('Sorry, connection issue. Try again.', 'bot');
    }
}

// Update addMessage to show response time
function addMessage(text, sender, responseTime = null) {
    const messagesContainer = document.getElementById('chatMessages');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    if (sender === 'bot') {
        const avatarDiv = document.createElement('div');
        avatarDiv.className = 'message-avatar';
        avatarDiv.innerHTML = '<i class="fas fa-robot"></i>';
        messageDiv.appendChild(avatarDiv);
    }
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    const bubbleDiv = document.createElement('div');
    bubbleDiv.className = 'message-bubble';
    bubbleDiv.innerHTML = formatMessage(text);
    
    const timeSpan = document.createElement('span');
    timeSpan.className = 'message-time';
    
    // Show response time for bot
    if (sender === 'bot' && responseTime) {
        timeSpan.innerHTML = `${new Date().toLocaleTimeString('en-US', { 
            hour: 'numeric', 
            minute: '2-digit' 
        })} • ⚡ ${responseTime}s`;
    } else {
        timeSpan.textContent = new Date().toLocaleTimeString('en-US', { 
            hour: 'numeric', 
            minute: '2-digit' 
        });
    }
    
    contentDiv.appendChild(bubbleDiv);
    contentDiv.appendChild(timeSpan);
    messageDiv.appendChild(contentDiv);
    
    if (sender === 'user') {
        const avatarDiv = document.createElement('div');
        avatarDiv.className = 'message-avatar';
        avatarDiv.innerHTML = '<i class="fas fa-user"></i>';
        messageDiv.appendChild(avatarDiv);
    }
    
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}