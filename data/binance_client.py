import os
import pandas as pd
import ccxt

def get_exchange():
    api = os.getenv("BINANCE_API_KEY", "")
    sec = os.getenv("BINANCE_API_SECRET", "")
    testnet = os.getenv("BINANCE_TESTNET", "true").lower() in ("1","true","yes")
    if testnet:
        return ccxt.binance({'apiKey': api, 'secret': sec, 'enableRateLimit': True,
                             'urls': {'api': 'https://testnet.binance.vision/api'}})
    return ccxt.binance({'apiKey': api, 'secret': sec, 'enableRateLimit': True})

def fetch_candles(symbol="BTC/USDT", timeframe="1m", limit=500):
    ex = get_exchange()
    ohlcv = ex.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['ts','open','high','low','close','volume'])
    df['ts'] = pd.to_datetime(df['ts'], unit='ms')
    return df

if __name__ == '__main__':
    print(fetch_candles())
