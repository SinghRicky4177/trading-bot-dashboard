from flask import Flask, render_template, jsonify, request
import yfinance as yf
import pandas as pd
from datetime import datetime
import time

app = Flask(__name__)

US_STOCKS = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA', 'V', 'ADBE', 'BAC',
    'AVGO', 'TXN', 'PLD', 'C', 'JPM', 'WMT', 'KO', 'PEP', 'NFLX', 'AMD',
    'INTC', 'CSCO', 'QCOM', 'IBM', 'ORCL', 'CRM', 'PYPL', 'DIS', 'COST', 'HD'
]

CANADIAN_STOCKS = [
    'RY.TO', 'TD.TO', 'ENB.TO', 'CNQ.TO', 'BNS.TO', 'BMO.TO', 'CM.TO', 'SHOP.TO',
    'SU.TO', 'CVE.TO', 'MFC.TO', 'SLF.TO', 'GIB.A.TO', 'T.TO', 'BCE.TO'
]

def calculate_rsi(prices, period=14):
    if len(prices) < period + 1:
        return 50
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1] if not pd.isna(rsi.iloc[-1]) else 50

def analyze_stock(ticker, market='US'):
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period="3mo")
        if len(df) < 50:
            return None
        df['SMA20'] = df['Close'].rolling(20).mean()
        df['SMA50'] = df['Close'].rolling(50).mean()
        rsi = calculate_rsi(df['Close'], 14)
        current_price = df['Close'].iloc[-1]
        sma20 = df['SMA20'].iloc[-1]
        sma50 = df['SMA50'].iloc[-1]
        score = 0
        if current_price > sma20: score += 1
        if current_price > sma50: score += 1
        if sma20 > sma50: score += 1
        if rsi < 35: score += 1
        elif rsi > 75: score -= 1
        if score >= 3:
            signal = "STRONG BUY"
            signal_class = "strong-buy"
            emoji = "🔥"
        elif score >= 2:
            signal = "BUY"
            signal_class = "buy"
            emoji = "✅"
        elif score <= -1:
            signal = "SELL"
            signal_class = "sell"
            emoji = "❌"
        else:
            signal = "HOLD"
            signal_class = "hold"
            emoji = "⏸️"
        info = stock.info
        name = info.get('longName', ticker)[:35]
        return {
            'ticker': ticker,
            'name': name,
            'market': market,
            'price': round(current_price, 2),
            'sma20': round(sma20, 2),
            'sma50': round(sma50, 2),
            'rsi': round(rsi, 1),
            'score': score,
            'signal': signal,
            'signal_class': signal_class,
            'emoji': emoji,
            'change_percent': round(((current_price - df['Close'].iloc[-6]) / df['Close'].iloc[-6]) * 100, 2) if len(df) >= 6 else 0
        }
    except Exception as e:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stocks')
def get_stocks():
    market = request.args.get('market', 'all')
    all_stocks = []
    if market in ['all', 'us']:
        for ticker in US_STOCKS:
            result = analyze_stock(ticker, 'US')
            if result:
                all_stocks.append(result)
            time.sleep(0.05)
    if market in ['all', 'canada']:
        for ticker in CANADIAN_STOCKS:
            result = analyze_stock(ticker, 'CAN')
            if result:
                all_stocks.append(result)
            time.sleep(0.05)
    all_stocks.sort(key=lambda x: x['score'], reverse=True)
    return jsonify({
        'stocks': all_stocks,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'total': len(all_stocks)
    })

@app.route('/api/stock/<ticker>')
def get_stock_detail(ticker):
    market = 'CAN' if '.TO' in ticker else 'US'
    result = analyze_stock(ticker, market)
    if result:
        stock = yf.Ticker(ticker)
        df = stock.history(period="2mo")
        result['history'] = {
            'dates': [d.strftime('%Y-%m-%d') for d in df.index[-30:]],
            'prices': [round(p, 2) for p in df['Close'].iloc[-30:].tolist()],
            'volumes': [int(v) for v in df['Volume'].iloc[-30:].tolist()]
        }
        return jsonify(result)
    return jsonify({'error': 'Stock not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
