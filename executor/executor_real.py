import time
from model.predict import predict
from config import settings

MODE = settings.MODE
SYMBOL = settings.DEFAULT_SYMBOL
SIZE = settings.DEFAULT_ORDER_SIZE

def place_market_order(side, amount):
    if MODE == 'SIMULATION':
        print(f"[SIM] Would place {side} {amount} {SYMBOL}")
        return {'status':'simulated','side':side,'amount':amount}
    # For REAL mode, implement exchange order here.
    print('[REAL mode not implemented]')
    return {'error':'real mode not implemented'}

def main_loop():
    print('Executor started in', MODE, 'mode for', SYMBOL)
    while True:
        pred = predict()
        if 'prob_up' in pred:
            p = pred['prob_up']
            print('Model prob up:', p)
            if p > 0.6:
                place_market_order('BUY', SIZE)
            elif p < 0.4:
                place_market_order('SELL', SIZE)
            else:
                print('No confident signal.')
        else:
            print('No model available.')
        time.sleep(60)

if __name__ == '__main__':
    main_loop()
