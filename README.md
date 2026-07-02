# Dialogflow Telegram Chatbot Backend

A Flask-based backend webhook for a Dialogflow chatbot that performs real-time currency conversion. It integrates with Telegram via Dialogflow and uses the Free Currency Converter API to fetch current conversion rates.

## Features

- **Dialogflow Integration**: Exposes a webhook endpoint (`/`) to receive fulfillment POST requests from Dialogflow.
- **Currency Conversion**: Extracts unit currency (source currency and amount) and target currency from Dialogflow parameters.
- **Real-Time Exchange Rates**: Fetches rates dynamically from the Free Currency Converter API.
- **Formatted Response**: Sends fulfillment messages back to Dialogflow which are then relayed to the user on Telegram.

## Project Structure

```text
├── app.py             # Flask application server and webhook logic
├── requirements.txt   # Python dependencies (Flask, requests)
├── Procfile           # Deployment configuration file
├── setup.sh           # Setup script for environment configuration
└── README.md          # Project documentation
```

## Getting Started

### Prerequisites

- Python 3.x
- A free API key from [Free Currency Converter API](https://free.currconv.com/)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/harxit13/ChatBot.git
   cd ChatBot
   ```

2. Set up a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running Locally

1. Start the Flask application:
   ```bash
   python app.py
   ```
   By default, the server will run on `http://127.0.0.1:5000/`.

2. To connect this to Dialogflow, you need a public URL. Use **ngrok** to expose your local port:
   ```bash
   ngrok http 5000
   ```
   Copy the `https` forwarding URL provided by ngrok and paste it into the **Fulfillment Webhook URL** section of your Dialogflow Console (e.g., `https://xxxx.ngrok.io/`).

## Dialogflow Configuration

- **Intent Parameter Mapping**:
  - The chatbot expects Dialogflow parameters:
    - `unit-currency`: A parameter containing `currency` (source currency) and `amount` (amount to convert).
    - `currency-name`: A parameter containing the target currency (e.g., `USD`, `INR`).
- **Fulfillment**:
  - Enable **Webhook fulfillment** for the intent that handles currency conversion so it sends the request to your backend.

## Configuration & API Key

Currently, the application uses a hardcoded API key in `app.py` for `free.currconv.com`. It is recommended to update the `apiKey` parameter or use environment variables to manage it securely.

## Note on Deployment (Procfile & setup.sh)

The repository currently includes a `Procfile` and `setup.sh` that seem configured for a Streamlit application (e.g. running `streamlit run app.py`). Since this project is a Flask application, you may want to update them before deploying to production (such as on Heroku):
1. Add `gunicorn` to `requirements.txt`.
2. Update `Procfile` to run a Flask WSGI server:
   ```yaml
   web: gunicorn app:app
   ```
