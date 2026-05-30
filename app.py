from flask import Flask, jsonify, render_template
import yfinance as yf
import pandas as pd
from datetime import datetime
import time

app = Flask(__name__)

US_STOCKS = ['AAPL', 'MSFT', 'GOOGL', 'NVDA', 'TSLA', 'META', 'AMZN']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/stocks')
def get_stocks():
    results = []
    for ticker in US_STOCKS:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="3mo")
            if len(hist) >= 20:
                sma20 = hist['Close'].rolling(20).mean().iloc[-1]
                sma50 = hist['Close'].rolling(50).mean().iloc[-1]
                current = hist['Close'].iloc[-1]
                score = 0
                if current > sma20: score += 1
                if current > sma50: score += 1
                if sma20 > sma50: score += 1
                signal = "BUY" if score >= 2 else "SELL" if score <= 0 else "HOLD"
                results.append({
                    'ticker': ticker,
                    'price': round(current,2),
                    'sma20': round(sma20,2),
                    'sma50': round(sma50,2),
                    'score': score,
                    'signal': signal
                })
            time.sleep(0.1)
        except:
            pass
    return jsonify({'stocks': results, 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
