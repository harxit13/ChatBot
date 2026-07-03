from flask import Flask,request,jsonify
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Chatbot Backend</title>
            <style>
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    background: linear-gradient(135deg, #74ebe1 0%, #89f7fe 100%);
                }
                .card {
                    background: white;
                    padding: 40px;
                    border-radius: 16px;
                    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
                    text-align: center;
                    max-width: 400px;
                }
                h1 {
                    color: #1a73e8;
                    margin-top: 0;
                    font-size: 24px;
                }
                p {
                    color: #5f6368;
                    font-size: 16px;
                    line-height: 1.5;
                }
                .status-badge {
                    display: inline-block;
                    background-color: #e6f4ea;
                    color: #137333;
                    padding: 6px 12px;
                    border-radius: 20px;
                    font-weight: bold;
                    margin-bottom: 20px;
                    font-size: 14px;
                }
            </style>
        </head>
        <body>
            <div class="card">
                <div class="status-badge">● Active</div>
                <h1>Chatbot Backend Running</h1>
                <p>Your Dialogflow Telegram webhook server is up and listening.</p>
                <p style="font-size: 13px; color: #9aa0a6;">Please send POST requests to this URL for Dialogflow fulfillment integration.</p>
            </div>
        </body>
        </html>
        """
    data = request.get_json()
    source_currency = data['queryResult']['parameters']['unit-currency']['currency']
    amount = data['queryResult']['parameters']['unit-currency']['amount']
    target_currency = data['queryResult']['parameters']['currency-name']


    cf = fetch_conversion_factor(source_currency,target_currency)
    final_amount = amount * cf
    final_amount = round(final_amount,2)
    response = {
        'fulfillmentText':"{} {} is {} {}".format(amount,source_currency,final_amount,target_currency)
    }
    return jsonify(response)

def fetch_conversion_factor(source,target):

    url = "https://free.currconv.com/api/v7/convert?q={}_{}&compact=ultra&apiKey=9aa0c54f5ad4c460c36d".format(source,target)

    response = requests.get(url)
    response = response.json()

    return response['{}_{}'.format(source,target)]


if __name__ == "__main__":
    app.run(debug=True)