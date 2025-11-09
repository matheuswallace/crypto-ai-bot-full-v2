import os, requests
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN','')
CHAT = os.getenv('TELEGRAM_CHAT_ID','')
def send(text):
    if not TOKEN or not CHAT:
        print('[Telegram] not configured')
        return
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    resp = requests.post(url, json={'chat_id':CHAT, 'text': text})
    print('Telegram:', resp.status_code, resp.text)
if __name__ == '__main__':
    send('Crypto AI Bot started (simulation)')
