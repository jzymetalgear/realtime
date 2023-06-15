import websocket
import json
import config
import requests
import time

# Define the WebSocket URL
url = 'wss://stream.data.alpaca.markets/v2/iex'

# Define the authentication payload
auth_payload = {
    'action': 'auth',
    'key': config.APCA_API_KEY_ID,
    'secret': config.APCA_API_SECRET_KEY
}

# Define the subscription payload for multiple stocks
subscription_payload = {
    'action': 'subscribe',
    'trades': ['AAPL', 'MSFT', 'GOOG']
}

def send_telegram_message(message):
    # ...
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print(f"Failed to send Telegram message: {response.text}")
    time.sleep(1)  # Add a 1-second delay before sending the next message
    
# Define the WebSocket connection callback functions
def on_open(ws):
    # Send the authentication payload
    ws.send(json.dumps(auth_payload))
    # Send the subscription payload
    ws.send(json.dumps(subscription_payload))
    # Send a Telegram bot message for successful connection
    send_telegram_message("Connecting successfully. Streaming real-time data live.")

def on_message(ws, message):
    # Parse and process the received message
    data = json.loads(message)
    # Extract the trade data for the subscribed stocks
    if data[0]['T'] == 't' and data[0]['S'] in subscription_payload['trades']:
        trade = data[0]
        symbol = trade['S']
        price = f"${float(trade['p']):.2f}"
        size = trade['s']
        timestamp = trade['t']
        # Print the trade information
        print(f"Symbol: {symbol}, Price: {price}, Size: {size}, Timestamp: {timestamp}")

def on_error(ws, error):
    print(f"WebSocket Error: {error}")
    # Send a Telegram bot message for connection failure
    send_telegram_message("Failed to connect to the WebSocket.")

def on_close(ws):
    print("WebSocket connection closed")
    # Send a Telegram bot message for connection closure
    send_telegram_message("WebSocket connection closed.")

# Function to send a message via Telegram bot
def send_telegram_message(message):
    bot_token = config.TELEGRAM_BOT_TOKEN
    chat_id = config.TELEGRAM_CHAT_ID
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print(f"Failed to send Telegram message: {response.text}")

# Start the WebSocket connection
ws = websocket.WebSocketApp(url,
                            on_open=on_open,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)

# Run the WebSocket connection
ws.run_forever()
