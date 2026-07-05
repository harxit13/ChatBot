from flask import Flask,request,jsonify
import requests

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
            <title>Currency Converter Bot</title>
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
            <style>
                :root {
                    --bg-gradient: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #020617 100%);
                    --panel-bg: rgba(30, 41, 59, 0.45);
                    --border-color: rgba(255, 255, 255, 0.08);
                    --text-primary: #f8fafc;
                    --text-secondary: #94a3b8;
                    --accent-color: #6366f1;
                    --accent-hover: #4f46e5;
                    --accent-glow: rgba(99, 102, 241, 0.4);
                    --bot-bubble-bg: rgba(255, 255, 255, 0.06);
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
                    filter: blur(100px);
                    opacity: 0.25;
                }
                .orb-1 {
                    top: 15%;
                    left: 20%;
                    width: 300px;
                    height: 300px;
                    background: #6366f1;
                }
                .orb-2 {
                    bottom: 15%;
                    right: 20%;
                    width: 350px;
                    height: 350px;
                    background: #ec4899;
                }

                /* Main Glassmorphic Container */
                .chat-container {
                    position: relative;
                    z-index: 10;
                    width: 90%;
                    max-width: 480px;
                    height: 85vh;
                    max-height: 700px;
                    background: var(--panel-bg);
                    backdrop-filter: blur(25px);
                    -webkit-backdrop-filter: blur(25px);
                    border: 1px solid var(--border-color);
                    border-radius: 24px;
                    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.35);
                    display: flex;
                    flex-direction: column;
                    overflow: hidden;
                    animation: fadeIn 0.6s cubic-bezier(0.16, 1, 0.3, 1) both;
                }

                @keyframes fadeIn {
                    from { opacity: 0; transform: translateY(20px); }
                    to { opacity: 1; transform: translateY(0); }
                }

                /* Header */
                .chat-header {
                    padding: 20px;
                    background: rgba(15, 23, 42, 0.4);
                    border-bottom: 1px solid var(--border-color);
                    display: flex;
                    align-items: center;
                    gap: 12px;
                }
                .bot-avatar {
                    width: 44px;
                    height: 44px;
                    background: linear-gradient(135deg, #818cf8 0%, #6366f1 100%);
                    border-radius: 14px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    box-shadow: 0 4px 12px var(--accent-glow);
                }
                .bot-avatar svg {
                    width: 24px;
                    height: 24px;
                    fill: white;
                }
                .bot-info {
                    flex-grow: 1;
                }
                .bot-name {
                    font-size: 16px;
                    font-weight: 600;
                    letter-spacing: -0.3px;
                }
                .bot-status {
                    display: flex;
                    align-items: center;
                    gap: 6px;
                    font-size: 12px;
                    color: var(--text-secondary);
                }
                .status-dot {
                    width: 8px;
                    height: 8px;
                    background-color: #10b981;
                    border-radius: 50%;
                    box-shadow: 0 0 8px #10b981;
                    animation: pulse 2s infinite;
                }

                @keyframes pulse {
                    0% { transform: scale(0.95); opacity: 0.5; }
                    50% { transform: scale(1.1); opacity: 1; }
                    100% { transform: scale(0.95); opacity: 0.5; }
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
                    width: 6px;
                }
                .messages-area::-webkit-scrollbar-track {
                    background: transparent;
                }
                .messages-area::-webkit-scrollbar-thumb {
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 10px;
                }

                /* Message Bubbles */
                .message {
                    max-width: 80%;
                    padding: 12px 18px;
                    border-radius: 18px;
                    font-size: 14px;
                    line-height: 1.5;
                    word-wrap: break-word;
                    animation: slideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1) both;
                }

                @keyframes slideUp {
                    from { opacity: 0; transform: translateY(10px); }
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
                    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.25);
                }

                /* Typing Indicator */
                .typing-indicator {
                    display: flex;
                    align-items: center;
                    gap: 4px;
                    padding: 12px 18px;
                }
                .typing-dot {
                    width: 6px;
                    height: 6px;
                    background: var(--text-secondary);
                    border-radius: 50%;
                    animation: bounce 1.3s infinite ease-in-out;
                }
                .typing-dot:nth-child(2) { animation-delay: 0.15s; }
                .typing-dot:nth-child(3) { animation-delay: 0.3s; }

                @keyframes bounce {
                    0%, 60%, 100% { transform: translateY(0); }
                    30% { transform: translateY(-6px); }
                }

                /* Quick Suggestions */
                .suggestions-container {
                    padding: 0 20px 10px;
                    display: flex;
                    gap: 8px;
                    overflow-x: auto;
                    white-space: nowrap;
                }
                .suggestions-container::-webkit-scrollbar {
                    display: none;
                }
                .suggestion-tag {
                    background: rgba(255, 255, 255, 0.04);
                    border: 1px solid var(--border-color);
                    padding: 8px 14px;
                    border-radius: 20px;
                    font-size: 13px;
                    cursor: pointer;
                    color: var(--text-secondary);
                    transition: all 0.2s ease;
                }
                .suggestion-tag:hover {
                    background: rgba(99, 102, 241, 0.15);
                    border-color: var(--accent-color);
                    color: var(--text-primary);
                }

                /* Input Bar */
                .input-container {
                    padding: 16px 20px 20px;
                    background: rgba(15, 23, 42, 0.3);
                    border-top: 1px solid var(--border-color);
                }
                .input-wrapper {
                    display: flex;
                    align-items: center;
                    background: rgba(255, 255, 255, 0.05);
                    border: 1px solid var(--border-color);
                    border-radius: 16px;
                    padding: 6px 6px 6px 16px;
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
                    font-size: 14px;
                    padding: 8px 0;
                }
                .chat-input::placeholder {
                    color: var(--text-secondary);
                }
                .send-btn {
                    width: 38px;
                    height: 38px;
                    background: var(--accent-color);
                    border: none;
                    border-radius: 12px;
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
                    width: 16px;
                    height: 16px;
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
                    <div class="bot-avatar">
                        <svg viewBox="0 0 24 24">
                            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/>
                        </svg>
                    </div>
                    <div class="bot-info">
                        <div class="bot-name">Currency Converter Bot</div>
                        <div class="bot-status">
                            <span class="status-dot"></span>
                            Online (Local Mock Mode)
                        </div>
                    </div>
                </div>

                <!-- Messages -->
                <div class="messages-area" id="messagesArea">
                    <div class="message message-bot">
                        Hi! I am your Currency Converter Bot. 💵💶
                        <br><br>
                        You can convert currency rates dynamically. Just ask me like:
                        <br>
                        <strong>"Convert 100 USD to INR"</strong> or <strong>"50 EUR to USD"</strong>.
                    </div>
                </div>

                <!-- Suggestions -->
                <div class="suggestions-container">
                    <div class="suggestion-tag" onclick="sendSuggestion('100 USD to INR')">💵 100 USD to INR</div>
                    <div class="suggestion-tag" onclick="sendSuggestion('50 EUR to USD')">💶 50 EUR to USD</div>
                    <div class="suggestion-tag" onclick="sendSuggestion('10 GBP to CAD')">💷 10 GBP to CAD</div>
                </div>

                <!-- Input -->
                <div class="input-container">
                    <form id="chatForm" onsubmit="handleSend(event)">
                        <div class="input-wrapper">
                            <input type="text" id="userInput" class="chat-input" placeholder="Type a message (e.g., 100 USD to INR)..." autocomplete="off">
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

                function appendMessage(text, isUser = false) {
                    const messageDiv = document.createElement('div');
                    messageDiv.classList.add('message');
                    messageDiv.classList.add(isUser ? 'message-user' : 'message-bot');
                    messageDiv.innerHTML = text;
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
                    // Regex matches: optionally "convert", then number, then 3 letter source currency, then "to" or "in" optionally, then 3 letter target currency
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

                    const parsed = parseInput(text);
                    if (!parsed) {
                        const indicator = showTypingIndicator();
                        setTimeout(() => {
                            removeTypingIndicator(indicator);
                            appendMessage("I couldn't parse your conversion request. Please try typing it like: <br><strong>'100 USD to INR'</strong> or click one of the quick suggestions below!");
                        }, 600);
                        return;
                    }

                    // Build standard Dialogflow payload to test the actual Flask backend endpoint
                    const payload = {
                        queryResult: {
                            parameters: {
                                "unit-currency": {
                                    currency: parsed.source,
                                    amount: parsed.amount
                                },
                                "currency-name": parsed.target
                            }
                        }
                    };

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
        data = request.get_json()
        source_currency = data['queryResult']['parameters']['unit-currency']['currency']
        amount = data['queryResult']['parameters']['unit-currency']['amount']
        target_currency = data['queryResult']['parameters']['currency-name']

        cf = fetch_conversion_factor(source_currency, target_currency)
        final_amount = amount * cf
        final_amount = round(final_amount, 2)
        response = {
            'fulfillmentText': "{} {} is {} {}".format(amount, source_currency, final_amount, target_currency)
        }
    except Exception as e:
        response = {
            'fulfillmentText': "Sorry, I couldn't perform the conversion. Error: {}".format(str(e))
        }
    return jsonify(response)

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