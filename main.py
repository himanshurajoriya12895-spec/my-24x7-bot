import requests
import os

try:
    token = os.getenv('8913665698:AAE4KqNbiJEM1VLnTIwXdOKuJGVteP2v0Tw')
    chat_id = os.getenv('8193076289')
    
    print(f"Token found: {bool(token)}")
    print(f"Chat ID found: {bool(chat_id)}")
    
    price = requests.get(
        "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT",
        timeout=10
    ).json()['price']
    
    print(f"BTC Price: {price}")
    
    r = requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        json={"chat_id": chat_id, "text": f"BTC: ${float(price):,.2f}"}
    )
    
    print(f"Telegram Response: {r.status_code}")
    print(f"Telegram Message: {r.text}")
    
except Exception as e:
    print(f"ERROR: {e}")
