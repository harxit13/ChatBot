from flask import Flask, request, jsonify
import requests
import google.generativeai as genai
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return r"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Universal AI Chatbot</title>
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
            <style>
                :root {
                    --bg-gradient: linear-gradient(135deg, #090d16 0%, #111827 50%, #05070c 100%);
                    --panel-bg: rgba(17, 24, 39, 0.5);
                    --border-color: rgba(255, 255, 255, 0.08);
                    --text-primary: #f3f4f6;
                    --text-secondary: #9ca3af;
                    --accent-color: #6366f1;
                    --accent-hover: #4f46e5;
                    --accent-glow: rgba(99, 102, 241, 0.35);
                    --bot-bubble-bg: rgba(255, 255, 255, 0.05);
                    --user-bubble-bg: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
                }

                * {
                    box-sizing: border-box;
                    margin: 0;
                    padding: 0;
                    font-family: 'Plus Jakarta Sans', sans-serif;
                }

                body {
                    background: var(--bg-gradient);
                    color: var(--text-primary);
                    height: 100vh;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    overflow: hidden;
                }

                /* Background Decorative Elements */
                .glowing-orbs {
                    position: absolute;
                    width: 100%;
                    height: 100%;
                    top: 0;
                    left: 0;
                    z-index: 1;
                    pointer-events: none;
                }
                .orb {
                    position: absolute;
                    border-radius: 50%;
                    filter: blur(120px);
                    opacity: 0.18;
                }
                .orb-1 {
                    top: 10%;
                    left: 15%;
                    width: 320px;
                    height: 320px;
                    background: #6366f1;
                }
                .orb-2 {
                    bottom: 10%;
                    right: 15%;
                    width: 380px;
                    height: 380px;
                    background: #d946ef;
                }

                /* Main Glassmorphic Container */
                .chat-container {
                    position: relative;
                    z-index: 10;
                    width: 90%;
                    max-width: 500px;
                    height: 88vh;
                    max-height: 750px;
                    background: var(--panel-bg);
                    backdrop-filter: blur(30px);
                    -webkit-backdrop-filter: blur(30px);
                    border: 1px solid var(--border-color);
                    border-radius: 28px;
                    box-shadow: 0 25px 60px rgba(0, 0, 0, 0.45);
                    display: flex;
                    flex-direction: column;
                    overflow: hidden;
                    animation: fadeIn 0.6s cubic-bezier(0.16, 1, 0.3, 1) both;
                }

                @keyframes fadeIn {
                    from { opacity: 0; transform: translateY(15px); }
                    to { opacity: 1; transform: translateY(0); }
                }

                /* Header */
                .chat-header {
                    padding: 16px 20px;
                    background: rgba(10, 15, 30, 0.45);
                    border-bottom: 1px solid var(--border-color);
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    gap: 12px;
                }
                .bot-profile {
                    display: flex;
                    align-items: center;
                    gap: 12px;
                }
                .bot-avatar {
                    width: 42px;
                    height: 42px;
                    background: linear-gradient(135deg, #a78bfa 0%, #6366f1 100%);
                    border-radius: 12px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    box-shadow: 0 4px 14px var(--accent-glow);
                }
                .bot-avatar svg {
                    width: 22px;
                    height: 22px;
                    fill: white;
                }
                .bot-info {
                    display: flex;
                    flex-direction: column;
                }
                .bot-name {
                    font-size: 15px;
                    font-weight: 600;
                    letter-spacing: -0.2px;
                }
                .bot-status {
                    display: flex;
                    align-items: center;
                    gap: 5px;
                    font-size: 11px;
                    color: var(--text-secondary);
                }
                .status-dot {
                    width: 7px;
                    height: 7px;
                    background-color: #10b981;
                    border-radius: 50%;
                    box-shadow: 0 0 6px #10b981;
                    animation: pulse 2s infinite;
                }

                @keyframes pulse {
                    0% { transform: scale(0.9); opacity: 0.5; }
                    50% { transform: scale(1.1); opacity: 1; }
                    100% { transform: scale(0.9); opacity: 0.5; }
                }

                /* Settings Panel */
                .settings-btn {
                    background: transparent;
                    border: none;
                    cursor: pointer;
                    padding: 8px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: var(--text-secondary);
                    transition: color 0.2s ease, transform 0.2s ease;
                    border-radius: 8px;
                }
                .settings-btn:hover {
                    color: var(--text-primary);
                    background: rgba(255, 255, 255, 0.04);
                }
                .settings-btn svg {
                    width: 20px;
                    height: 20px;
                    fill: currentColor;
                }
                .settings-drawer {
                    background: rgba(10, 15, 30, 0.7);
                    border-bottom: 1px solid var(--border-color);
                    padding: 16px 20px;
                    display: none;
                    flex-direction: column;
                    gap: 8px;
                    font-size: 12px;
                    animation: slideDown 0.3s cubic-bezier(0.16, 1, 0.3, 1) both;
                }
                @keyframes slideDown {
                    from { transform: translateY(-10px); opacity: 0; }
                    to { transform: translateY(0); opacity: 1; }
                }
                .settings-drawer label {
                    font-weight: 500;
                    color: var(--text-primary);
                }
                .key-input-wrapper {
                    display: flex;
                    gap: 8px;
                }
                .key-input {
                    flex-grow: 1;
                    background: rgba(0, 0, 0, 0.2);
                    border: 1px solid var(--border-color);
                    border-radius: 8px;
                    padding: 8px 12px;
                    color: var(--text-primary);
                    font-size: 12px;
                    outline: none;
                }
                .key-input:focus {
                    border-color: var(--accent-color);
                }
                .settings-drawer a {
                    color: #818cf8;
                    text-decoration: none;
                }
                .settings-drawer a:hover {
                    text-decoration: underline;
                }

                /* Chat Messages Area */
                .messages-area {
                    flex-grow: 1;
                    padding: 20px;
                    overflow-y: auto;
                    display: flex;
                    flex-direction: column;
                    gap: 16px;
                    scroll-behavior: smooth;
                }

                /* Custom Scrollbar */
                .messages-area::-webkit-scrollbar {
                    width: 5px;
                }
                .messages-area::-webkit-scrollbar-track {
                    background: transparent;
                }
                .messages-area::-webkit-scrollbar-thumb {
                    background: rgba(255, 255, 255, 0.08);
                    border-radius: 10px;
                }

                /* Message Bubbles */
                .message {
                    max-width: 85%;
                    padding: 12px 16px;
                    border-radius: 18px;
                    font-size: 13.5px;
                    line-height: 1.5;
                    word-wrap: break-word;
                    animation: slideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1) both;
                    white-space: pre-wrap;
                }

                @keyframes slideUp {
                    from { opacity: 0; transform: translateY(8px); }
                    to { opacity: 1; transform: translateY(0); }
                }

                .message-bot {
                    background: var(--bot-bubble-bg);
                    border: 1px solid var(--border-color);
                    align-self: flex-start;
                    border-bottom-left-radius: 4px;
                    color: var(--text-primary);
                }

                .message-user {
                    background: var(--user-bubble-bg);
                    align-self: flex-end;
                    border-bottom-right-radius: 4px;
                    color: white;
                    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.2);
                }

                /* Typing Indicator */
                .typing-indicator {
                    display: flex;
                    align-items: center;
                    gap: 4px;
                    padding: 12px 16px;
                }
                .typing-dot {
                    width: 5px;
                    height: 5px;
                    background: var(--text-secondary);
                    border-radius: 50%;
                    animation: bounce 1.3s infinite ease-in-out;
                }
                .typing-dot:nth-child(2) { animation-delay: 0.15s; }
                .typing-dot:nth-child(3) { animation-delay: 0.3s; }

                @keyframes bounce {
                    0%, 60%, 100% { transform: translateY(0); }
                    30% { transform: translateY(-5px); }
                }

                /* Suggestions */
                .suggestions-container {
                    padding: 0 20px 8px;
                    display: flex;
                    gap: 8px;
                    overflow-x: auto;
                    white-space: nowrap;
                }
                .suggestions-container::-webkit-scrollbar {
                    display: none;
                }
                .suggestion-tag {
                    background: rgba(255, 255, 255, 0.03);
                    border: 1px solid var(--border-color);
                    padding: 6px 12px;
                    border-radius: 20px;
                    font-size: 12px;
                    cursor: pointer;
                    color: var(--text-secondary);
                    transition: all 0.2s ease;
                }
                .suggestion-tag:hover {
                    background: rgba(99, 102, 241, 0.12);
                    border-color: var(--accent-color);
                    color: var(--text-primary);
                }

                /* Input Bar */
                .input-container {
                    padding: 14px 20px 20px;
                    background: rgba(10, 15, 30, 0.3);
                    border-top: 1px solid var(--border-color);
                }
                .input-wrapper {
                    display: flex;
                    align-items: center;
                    background: rgba(255, 255, 255, 0.04);
                    border: 1px solid var(--border-color);
                    border-radius: 14px;
                    padding: 4px 4px 4px 14px;
                    transition: border-color 0.3s ease, box-shadow 0.3s ease;
                }
                .input-wrapper:focus-within {
                    border-color: var(--accent-color);
                    box-shadow: 0 0 10px var(--accent-glow);
                }
                .chat-input {
                    flex-grow: 1;
                    background: transparent;
                    border: none;
                    outline: none;
                    color: var(--text-primary);
                    font-size: 13.5px;
                    padding: 8px 0;
                }
                .chat-input::placeholder {
                    color: var(--text-secondary);
                }
                .send-btn {
                    width: 36px;
                    height: 36px;
                    background: var(--accent-color);
                    border: none;
                    border-radius: 10px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    cursor: pointer;
                    transition: background 0.2s ease, transform 0.1s ease;
                }
                .send-btn:hover {
                    background: var(--accent-hover);
                }
                .send-btn:active {
                    transform: scale(0.95);
                }
                .send-btn svg {
                    width: 15px;
                    height: 15px;
                    fill: white;
                }
            </style>
        </head>
        <body>
            <div class="glowing-orbs">
                <div class="orb orb-1"></div>
                <div class="orb orb-2"></div>
            </div>

            <div class="chat-container">
                <!-- Header -->
                <div class="chat-header">
                    <div class="bot-profile">
                        <div class="bot-avatar">
                            <svg viewBox="0 0 24 24">
                                <path d="M21 11.5a8.38 8.38 0 01-.9 3.8 8.5 8.5 0 01-7.6 4.7 8.38 8.38 0 01-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 01-.9-3.8 8.5 8.5 0 014.7-7.6 8.38 8.38 0 013.8-.9h.5a8.48 8.48 0 018 8v.5zM12 7v6h4"/>
                            </svg>
                        </div>
                        <div class="bot-info">
                            <div class="bot-name">AI Assistant Bot</div>
                            <div class="bot-status">
                                <span class="status-dot"></span>
                                Online (Gemini Powered)
                            </div>
                        </div>
                    </div>
                    <button class="settings-btn" onclick="toggleSettings()" title="Settings & API Key">
                        <svg viewBox="0 0 24 24">
                            <path d="M19.14 12.94c.04-.3c.06-.61.06-1.17.06-1.75 0-.58-.02-1.14-.06-1.75l2.1-1.64c.2-.15.25-.42.12-.64l-2-3.46c-.12-.22-.39-.3-.61-.22l-2.49 1a8.65 8.65 0 00-3-1.74l-.38-2.65A.488.488 0 0012.4 1h-4c-.22 0-.42.17-.45.4l-.38 2.65c-.09.3-.57.85-1.4 1.34L3.68 3.39c-.22-.08-.49 0-.61.22l-2 3.46c-.13.22-.07.49.12.64l2.11 1.65c-.04.32-.07.65-.07 1.11 0 .47.02.93.07 1.4L1.1 13.51c-.19.15-.24.42-.12.64l2 3.46c.12.22.39.3.61.22l2.49-1a8.65 8.65 0 003 1.74l.38 2.65c.03.23.23.4.45.4h4c.22 0 .42-.17.45-.4l.38-2.65c.09-.3.57-.85 1.4-1.34l2.49 1c.22.08.49 0 .61-.22l2-3.46c.12-.22.07-.49-.12-.64l-2.11-1.65zM12 15.5c-1.93 0-3.5-1.57-3.5-3.5s1.57-3.5 3.5-3.5 3.5 1.57 3.5 3.5-1.57 3.5-3.5 3.5z"/>
                        </svg>
                    </button>
                </div>

                <!-- Settings Drawer -->
                <div class="settings-drawer" id="settingsDrawer">
                    <label for="apiKeyInput">Gemini API Key</label>
                    <div class="key-input-wrapper">
                        <input type="password" id="apiKeyInput" class="key-input" placeholder="AI Studio API key (AIzaSy...)" onchange="saveApiKey()">
                    </div>
                    <span style="color: var(--text-secondary)">Get a free API key from <a href="https://aistudio.google.com/" target="_blank">Google AI Studio</a>. Keys are stored locally in your browser.</span>
                </div>

                <!-- Messages -->
                <div class="messages-area" id="messagesArea">
                    <div class="message message-bot">
                        Hi! I am your AI Chatbot. 🤖✨
                        <br><br>
                        Now you can **ask me anything**! 
                        <br>
                        For example:
                        <ul>
                            <li>"Write a poem about coding"</li>
                            <li>"Explain recursion in 2 sentences"</li>
                            <li>"Convert 100 USD to INR" (runs local rates)</li>
                        </ul>
                    </div>
                </div>

                <!-- Suggestions -->
                <div class="suggestions-container">
                    <div class="suggestion-tag" onclick="sendSuggestion('Write a short coding joke')">😂 Write a Joke</div>
                    <div class="suggestion-tag" onclick="sendSuggestion('Convert 50 EUR to USD')">💶 50 EUR to USD</div>
                    <div class="suggestion-tag" onclick="sendSuggestion('Explain photosyntehsis simply')">🌱 Explain Photosynthesis</div>
                </div>

                <!-- Input -->
                <div class="input-container">
                    <form id="chatForm" onsubmit="handleSend(event)">
                        <div class="input-wrapper">
                            <input type="text" id="userInput" class="chat-input" placeholder="Ask me anything..." autocomplete="off">
                            <button type="submit" class="send-btn">
                                <svg viewBox="0 0 24 24">
                                    <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
                                </svg>
                            </button>
                        </div>
                    </form>
                </div>
            </div>

            <script>
                const messagesArea = document.getElementById('messagesArea');
                const userInput = document.getElementById('userInput');
                const settingsDrawer = document.getElementById('settingsDrawer');
                const apiKeyInput = document.getElementById('apiKeyInput');

                // Load API Key on start
                window.onload = () => {
                    const savedKey = localStorage.getItem('gemini_api_key');
                    if (savedKey) {
                        apiKeyInput.value = savedKey;
                    }
                };

                function toggleSettings() {
                    if (settingsDrawer.style.display === 'none' || !settingsDrawer.style.display) {
                        settingsDrawer.style.display = 'flex';
                    } else {
                        settingsDrawer.style.display = 'none';
                    }
                }

                function saveApiKey() {
                    const val = apiKeyInput.value.trim();
                    if (val) {
                        localStorage.setItem('gemini_api_key', val);
                    } else {
                        localStorage.removeItem('gemini_api_key');
                    }
                }

                function appendMessage(text, isUser = false) {
                    const messageDiv = document.createElement('div');
                    messageDiv.classList.add('message');
                    messageDiv.classList.add(isUser ? 'message-user' : 'message-bot');
                    
                    // Simple Markdown Parsing for response
                    let parsedText = text
                        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                        .replace(/\*(.*?)\*/g, '<em>$1</em>')
                        .replace(/`(.*?)`/g, '<code>$1</code>');
                    
                    messageDiv.innerHTML = parsedText;
                    messagesArea.appendChild(messageDiv);
                    messagesArea.scrollTop = messagesArea.scrollHeight;
                }

                function showTypingIndicator() {
                    const indicator = document.createElement('div');
                    indicator.id = 'typingIndicator';
                    indicator.classList.add('message', 'message-bot', 'typing-indicator');
                    indicator.innerHTML = `
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                    `;
                    messagesArea.appendChild(indicator);
                    messagesArea.scrollTop = messagesArea.scrollHeight;
                    return indicator;
                }

                function removeTypingIndicator(indicator) {
                    if (indicator && indicator.parentNode) {
                        indicator.parentNode.removeChild(indicator);
                    }
                }

                function parseInput(text) {
                    const regex = /(?:convert\s+)?(\d+(?:\.\d+)?)\s*([a-zA-Z]{3})\s*(?:to|in)?\s*([a-zA-Z]{3})/i;
                    const match = text.match(regex);
                    if (match) {
                        return {
                            amount: parseFloat(match[1]),
                            source: match[2].toUpperCase(),
                            target: match[3].toUpperCase()
                        };
                    }
                    return null;
                }

                async function handleSend(event) {
                    if (event) event.preventDefault();
                    const text = userInput.value.trim();
                    if (!text) return;

                    appendMessage(text, true);
                    userInput.value = '';

                    const apiKey = localStorage.getItem('gemini_api_key') || '';
                    let payload;
                    const parsedCurrency = parseInput(text);

                    if (parsedCurrency) {
                        payload = {
                            queryText: text,
                            apiKey: apiKey,
                            queryResult: {
                                parameters: {
                                    "unit-currency": {
                                        currency: parsedCurrency.source,
                                        amount: parsedCurrency.amount
                                    },
                                    "currency-name": parsedCurrency.target
                                }
                            }
                        };
                    } else {
                        payload = {
                            queryText: text,
                            apiKey: apiKey,
                            queryResult: {
                                parameters: {}
                            }
                        };
                    }

                    const indicator = showTypingIndicator();

                    try {
                        const response = await fetch('/', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify(payload)
                        });

                        const data = await response.json();
                        removeTypingIndicator(indicator);

                        if (data && data.fulfillmentText) {
                            appendMessage(data.fulfillmentText);
                        } else {
                            appendMessage("Received an unexpected response format from the server.");
                        }
                    } catch (error) {
                        removeTypingIndicator(indicator);
                        appendMessage("Error communicating with the webhook backend: " + error.message);
                    }
                }

                function sendSuggestion(text) {
                    userInput.value = text;
                    handleSend();
                }
            </script>
        </body>
        </html>
        """
    try:
        data = request.get_json() or {}
        query_text = data.get('queryText', '')
        user_api_key = data.get('apiKey', '')

        # Check Dialogflow parameters
        query_result = data.get('queryResult', {})
        params = query_result.get('parameters', {})
        
        if params and 'unit-currency' in params and 'currency-name' in params:
            source_currency = params['unit-currency']['currency']
            amount = params['unit-currency']['amount']
            target_currency = params['currency-name']

            cf = fetch_conversion_factor(source_currency, target_currency)
            final_amount = amount * cf
            final_amount = round(final_amount, 2)
            fulfillment_text = "{} {} is {} {}".format(amount, source_currency, final_amount, target_currency)
        else:
            fulfillment_text = generate_ai_response(query_text, user_api_key)

        response = {
            'fulfillmentText': fulfillment_text
        }
    except Exception as e:
        response = {
            'fulfillmentText': "Sorry, I couldn't process your request. Error: {}".format(str(e))
        }
    return jsonify(response)

def generate_ai_response(prompt, api_key=None):
    # Fallback order: user-supplied browser key -> local environment key
    key = api_key or os.environ.get("GEMINI_API_KEY")
    if not key:
        return "I can do currency conversions right now! To enable general chatbot replies, please click the gear/settings icon ⚙️ at the top right of this chat window and paste your free **Gemini API Key**."
        
    try:
        genai.configure(api_key=key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return "Failed to query Gemini API: {}".format(str(e))

def fetch_conversion_factor(source, target):
    source = source.upper()
    target = target.upper()
    
    if source == target:
        return 1.0
    
    url = "https://api.frankfurter.dev/v1/latest?base={}&symbols={}".format(source, target)
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError("Unsupported currency or API error (status code {})".format(response.status_code))
    
    data = response.json()
    if 'rates' not in data or target not in data['rates']:
        raise ValueError("Conversion rate not found for {} to {}".format(source, target))
        
    return data['rates'][target]


if __name__ == "__main__":
    app.run(debug=True)