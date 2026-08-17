import yfinance as yf
import pandas as pd
import requests
import os

# Telegram Alert (Jo tu Secrets mein daalega)
def send_telegram(message):
    token = os.getenv('8913665698:AAE4KqNbiJEM1VLnTIwXdOKuJGVteP2v0Tw')
    chat_id = os.getenv('8193076289')
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": message, "parse_mode": "HTML"})

def scan_market():
    # EURUSD data uthana (Bina kisi MT5 login ke)
    data = yf.download(tickers='EURUSD=X', period='5d', interval='60m')
    
    if data.empty:
        return
        
    df = data.copy()
    df.columns = ['open', 'high', 'low', 'close', 'adj_close', 'volume']
    
    # --- TERA SMC LOGIC (Indra-Jaal) ---
    df['liq_sweep_high'] = (df['high'] > df['high'].shift(1)) & (df['close'] < df['high'].shift(1))
    df['liq_sweep_low'] = (df['low'] < df['low'].shift(1)) & (df['close'] > df['low'].shift(1))
    
    last_row = df.iloc[-1]
    
    # Notification Logic
    if last_row['liq_sweep_low']:
        send_telegram(f"🟢 <b>BUY SIGNAL</b>\nEURUSD Price: {last_row['close']:.5f}\nLogic: Liquidity Sweep Low")
    elif last_row['liq_sweep_high']:
        send_telegram(f"🔴 <b>SELL SIGNAL</b>\nEURUSD Price: {last_row['close']:.5f}\nLogic: Liquidity Sweep High")
    else:
        print("No Signal Found.")

if __name__ == "__main__":
    scan_market()
