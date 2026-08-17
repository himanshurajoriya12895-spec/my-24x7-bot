import ccxt
import requests
from datetime import datetime

# ========== CONFIG ==========
BOT_TOKEN = "8913665698:AAE4KqNbiJEM1VLnTIwXdOKuJGVteP2v0Tw"
CHAT_ID = "8193076289"
SYMBOL = 'BTC/USDT'
# ============================

exchange = ccxt.binance()

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    })

def get_liquidity_data():
    try:
        # 1. Order Book
        ob = exchange.fetch_order_book(SYMBOL, limit=20)
        bids = ob['bids']
        asks = ob['asks']

        total_buy_vol = sum([b[1] for b in bids])
        total_sell_vol = sum([a[1] for a in asks])

        # 2. Imbalance Ratio
        imbalance = total_buy_vol / total_sell_vol

        # 3. Recent Trades
        trades = exchange.fetch_trades(SYMBOL, limit=50)
        recent_buys = sum([t['amount'] for t in trades if t['side'] == 'buy'])
        recent_sells = sum([t['amount'] for t in trades if t['side'] == 'sell'])

        # 4. Price
        price = exchange.fetch_ticker(SYMBOL)['last']

        time_now = datetime.now().strftime('%H:%M:%S')

        # 5. Oracle Decision
        if imbalance < 0.5 and recent_buys > recent_sells:
            msg = f"""
💀 <b>MAYA DETECTED - SHORT SIGNAL</b>
⏰ Time: {time_now}
💰 BTC Price: ${price:,.2f}
📊 Buy Liquidity: {total_buy_vol:.2f} BTC
📊 Sell Liquidity: {total_sell_vol:.2f} BTC
⚡ Buyers: {recent_buys:.2f} vs Sellers: {recent_sells:.2f}
🎯 Strategy: Fake pump expected. Whales dumping soon.
            """
            send_telegram(msg)

        elif imbalance > 2.0 and recent_sells > recent_buys:
            msg = f"""
🔥 <b>BHEDA DETECTED - LONG SIGNAL</b>
⏰ Time: {time_now}
💰 BTC Price: ${price:,.2f}
📊 Buy Liquidity: {total_buy_vol:.2f} BTC
📊 Sell Liquidity: {total_sell_vol:.2f} BTC
⚡ Buyers: {recent_buys:.2f} vs Sellers: {recent_sells:.2f}
🎯 Strategy: Whales absorbing. Bottom trap. LONG now.
            """
            send_telegram(msg)

        else:
            print(f"[{time_now}] No signal. Whales indecisive.")

    except Exception as e:
        send_telegram(f"❌ Oracle Error: {str(e)}")

# Single execution (GitHub Actions karега schedule)
get_liquidity_data()
