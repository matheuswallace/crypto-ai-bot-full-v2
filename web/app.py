from flask import Flask, jsonify, render_template_string
from model.predict import predict
from data.binance_client import fetch_candles
import os, threading, time

app = Flask(__name__)
TEMPLATE = """<!doctype html><title>Crypto AI Bot</title><h1>Crypto AI Bot — Dashboard (simulação)</h1>
<p>Symbol: {{symbol}}</p><p>Model prediction: {{pred}}</p><h3>Últimos closes</h3><pre>{{closes}}</pre>"""

def start_executor_background():
    try:
        from executor.executor_real import main_loop
    except Exception as e:
        print('Failed to import executor:', e)
        return
    t = threading.Thread(target=main_loop, daemon=True)
    t.start()
    print('Executor background thread started.')

@app.before_first_request
def startup():
    # start background executor
    start_executor_background()

@app.route('/')
def index():
    symbol = os.getenv('DEFAULT_SYMBOL','BTC/USDT')
    pred = predict()
    df = fetch_candles(symbol, timeframe='5m', limit=20)
    closes = df['close'].tolist()
    return render_template_string(TEMPLATE, symbol=symbol, pred=pred, closes=closes)

@app.route('/api/predict')
def api_predict():
    return jsonify(predict())

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
