import os
import sys
import threading
from flask import Flask, jsonify, render_template

# Corrige o caminho de importação
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importa o executor
from executor.executor_real import run_executor

app = Flask(__name__)

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
