from flask import Flask, jsonify, render_template, request
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import time
from stock_lists import ALL_STOCKS  # <-- our new file

app = Flask(__name__)

# Simple cache: store results for 30 minutes
cache = {
    'data': None,
    'timestamp': None
}
CACHE_DURATION = timedelta(minutes=30)

def calculate_rsi(prices, period=14):
    if len(prices) < period + 1:
        return 50
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1] if not pd.isna(rsi.iloc[-1]) else 50

def analyze_all_stocks():
    """Analyze all stocks and return list"""
    results = []
    total = len(ALL_STOCKS)
    for idx, ticker in enumerate(ALL_STOCKS):
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="3mo")
            if len(hist) < 50:
                continue

            info = stock.info
            name = info.get('longName', ticker)[:30]

            hist['SMA20'] = hist['Close'].rolling(20).mean()
            hist['SMA50'] = hist['Close'].rolling(50).mean()
            rsi = calculate_rsi(hist['Close'])

            current = hist['Close'].iloc[-1]
            sma20 = hist['SMA20'].iloc[-1]
            sma50 = hist['SMA50'].iloc[-1]

            score = 0
            if current > sma20: score += 1
            if current > sma50: score += 1
            if sma20 > sma50: score += 1
            if rsi < 35: score += 1
            elif rsi > 75: score -= 1

            if score >= 3:
                signal, sig_class, emoji = "STRONG BUY", "strong-buy", "🔥"
            elif score >= 2:
                signal, sig_class, emoji = "BUY", "buy", "✅"
            elif score <= -1:
                signal, sig_class, emoji = "SELL", "sell", "❌"
            else:
                signal, sig_class, emoji = "HOLD", "hold", "⏸️"

            results.append({
                'ticker': ticker,
                'name': name,
                'price': round(current, 2),
                'sma20': round(sma20, 2),
                'sma50': round(sma50, 2),
                'rsi': round(rsi, 1),
                'score': score,
                'signal': signal,
                'signal_class': sig_class,
                'emoji': emoji
            })
            # Small delay to avoid rate limit
            time.sleep(0.05)

            # Print progress every 50 stocks (visible in logs)
            if (idx+1) % 50 == 0:
                print(f"Processed {idx+1}/{total} stocks...")

        except Exception as e:
            print(f"Skipping {ticker}: {e}")
            continue

    results.sort(key=lambda x: x['score'], reverse=True)
    return results

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/stocks')
def get_stocks():
    # Use cache if fresh
    if cache['data'] and cache['timestamp'] and datetime.now() - cache['timestamp'] < CACHE_DURATION:
        all_results = cache['data']
        print("Returning cached data")
    else:
        print("Scanning all stocks (this will take ~3-5 minutes)...")
        all_results = analyze_all_stocks()
        cache['data'] = all_results
        cache['timestamp'] = datetime.now()

    # Support pagination (load only first 100 on frontend)
    limit = request.args.get('limit', default=100, type=int)
    page = request.args.get('page', default=1, type=int)
    start = (page - 1) * limit
    end = start + limit
    paginated = all_results[start:end]

    return jsonify({
        'stocks': paginated,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'total': len(all_results),
        'page': page,
        'pages': (len(all_results) + limit - 1) // limit
    })

if __name__ == '__main__':
    print(f"Starting with {len(ALL_STOCKS)} total stocks")
    app.run(host='0.0.0.0', port=5000)
