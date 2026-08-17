import MetaTrader5 as mt5
import pandas as pd
import requests
import os

# Telegram Alert Function
def send_telegram(message):
    token = os.getenv('8913665698:AAE4KqNbiJEM1VLnTIwXdOKuJGVteP2v0Tw')
    chat_id = os.getenv('8193076289')
    requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                  json={"chat_id": chat_id, "text": message})

# 1. MT5 Connection
login = int(os.getenv('MT5_LOGIN'))
password = os.getenv('MT5_PASS')
server = os.getenv('MT5_SERVER')

if not mt5.initialize(login=login, password=password, server=server):
    send_telegram("❌ MT5 Failed to Initialize")
    quit()

# 2. Data & Logic
symbol = "EURUSD"
rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_H1, 0, 100)
df = pd.DataFrame(rates)

# 3. SMC Logic (Tera Original)
df['liq_sweep_low'] = (df['low'] < df['low'].shift(1)) & (df['close'] > df['low'].shift(1))
df['liq_sweep_high'] = (df['high'] > df['high'].shift(1)) & (df['close'] < df['high'].shift(1))

last_row = df.iloc[-1]

# 4. Execution / Alert
if last_row['liq_sweep_low']:
    send_telegram(f"🟢 BUY SIGNAL: {symbol} at {last_row['close']}")
elif last_row['liq_sweep_high']:
    send_telegram(f"🔴 SELL SIGNAL: {symbol} at {last_row['close']}")
else:
    print("No signal, system active.")

mt5.shutdown()
