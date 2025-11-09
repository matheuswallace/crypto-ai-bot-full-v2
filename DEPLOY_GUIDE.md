DEPLOY GUIDE (Railway)

1. Push this repository to GitHub.
2. Go to https://railway.app and 'New Project' -> 'Deploy from GitHub' and select this repo.
3. Add Environment Variables in Railway (at minimum):
   - BINANCE_API_KEY
   - BINANCE_API_SECRET
   - BINANCE_TESTNET=true
   - MODE=SIMULATION
   - DEFAULT_SYMBOL=BTC/USDT
   - DEFAULT_ORDER_SIZE=0.001
   - MODEL_PATH=models/model.joblib
   - TELEGRAM_BOT_TOKEN (optional)
   - TELEGRAM_CHAT_ID (optional)
4. Deploy. Railway will install requirements and run the Procfile command (web: python web/app.py).
5. The web process launches Flask and starts the executor loop in a background thread. Monitor logs for both web and executor output.
