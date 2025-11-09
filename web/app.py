# Importa o executor que roda em segundo plano
from executor.executor_real import run_executor
from flask import Flask, jsonify, render_template_string
import sys, os
# Garante que a pasta raiz do projeto está no caminho
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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

# Inicia o executor assim que o app começa (Flask 3.x não tem before_first_request)
@app.before_request
def start_executor_once():
    if not getattr(app, "_executor_started", False):
        executor_thread = threading.Thread(target=run_executor)
        executor_thread.daemon = True
        executor_thread.start()
        app._executor_started = True


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
