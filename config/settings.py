import os
MODE = os.getenv("MODE", "SIMULATION")  # SIMULATION or REAL
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY", "")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET", "")
BINANCE_TESTNET = os.getenv("BINANCE_TESTNET", "true").lower() in ("1","true","yes")
DEFAULT_SYMBOL = os.getenv("DEFAULT_SYMBOL", "BTC/USDT")
DEFAULT_ORDER_SIZE = float(os.getenv("DEFAULT_ORDER_SIZE", "0.001"))
MODEL_PATH = os.getenv("MODEL_PATH", "models/model.joblib")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
