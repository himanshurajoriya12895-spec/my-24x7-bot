import requests
import os
import sys

try:
    token = os.environ.get('8913665698:AAE4KqNbiJEM1VLnTIwXdOKuJGVteP2v0Tw')
    chat_id = os.environ.get('8193076289')
    
    if not token or not chat_id:
        print("❌ ERROR: Secrets (BOT_TOKEN or CHAT_ID) are missing!")
        sys.exit(1)

    # BTC Price uthana
    res = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=20)
    price_data = res.json()
    price = float(price_data['price'])
    
    # Telegram bhejna
    msg = f"₿ BTC Price: ${price:,.2f}"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": msg}
    
    telegram_res = requests.post(url, json=payload)
    
    if telegram_res.status_code == 200:
        print("✅ Success: Message sent to Telegram!")
    else:
        print(f"❌ Telegram Error: {telegram_res.text}")
        sys.exit(1)

except Exception as e:
    print(f"❌ Script Crashed: {str(e)}")
    sys.exit(1)
