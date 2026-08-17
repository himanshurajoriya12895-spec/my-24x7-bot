import requests
import os

token = os.getenv('8913665698:AAE4KqNbiJEM1VLnTIwXdOKuJGVteP2v0Tw')
chat_id = os.getenv('8193076289')

price = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT").json()['price']

requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
              json={"chat_id": chat_id, "text": f"BTC: ${float(price):,.2f}"})
