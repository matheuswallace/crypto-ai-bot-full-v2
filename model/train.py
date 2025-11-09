import os, joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from data.binance_client import fetch_candles

MODEL_PATH = os.getenv("MODEL_PATH", "models/model.joblib")
SYMBOL = os.getenv("DEFAULT_SYMBOL", "BTC/USDT")

def featurize(df):
    df = df.copy()
    df['ret'] = df['close'].pct_change()
    df['ema9'] = df['close'].ewm(span=9).mean()
    df['ema21'] = df['close'].ewm(span=21).mean()
    df['rsi'] = (100 - (100 / (1 + (df['ret'].rolling(14).mean() / df['ret'].rolling(14).std())))).fillna(50)
    df = df.dropna()
    X = df[['close','ema9','ema21','rsi']].values
    y = (df['close'].shift(-1) > df['close']).astype(int)[:-1]
    X = X[:-1]
    return X, y

def train():
    df = fetch_candles(SYMBOL, timeframe='5m', limit=1000)
    X, y = featurize(df)
    if len(X)==0:
        raise RuntimeError('Not enough data')
    model = RandomForestClassifier(n_estimators=50, max_depth=5, random_state=42)
    model.fit(X,y)
    os.makedirs(os.path.dirname(MODEL_PATH) or '.', exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print('Model trained and saved at', MODEL_PATH)

if __name__ == '__main__':
    train()
