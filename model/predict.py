import os, joblib
from data.binance_client import fetch_candles
MODEL_PATH = os.getenv("MODEL_PATH", "models/model.joblib")
SYMBOL = os.getenv("DEFAULT_SYMBOL", "BTC/USDT")

def featurize_latest(df):
    df = df.copy()
    df['ret'] = df['close'].pct_change()
    df['ema9'] = df['close'].ewm(span=9).mean()
    df['ema21'] = df['close'].ewm(span=21).mean()
    df['rsi'] = (100 - (100 / (1 + (df['ret'].rolling(14).mean() / df['ret'].rolling(14).std())))).fillna(50)
    df = df.dropna()
    X = df[['close','ema9','ema21','rsi']].values
    return X[-1].reshape(1,-1)

def predict():
    import os
    if not os.path.exists(MODEL_PATH):
        return {'error':'model not found'}
    model = joblib.load(MODEL_PATH)
    df = fetch_candles(SYMBOL, timeframe='5m', limit=200)
    x = featurize_latest(df)
    p = float(model.predict_proba(x)[0,1])
    return {'prob_up': p}

if __name__ == '__main__':
    print(predict())
