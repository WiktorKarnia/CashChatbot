from flask import Flask, render_template, request, jsonify
import requests
import json
import logging
from chatbot import get_response  # Importowanie funkcji chatbota
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Załadowanie konfiguracji z pliku .env
load_dotenv('.config')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_API_URL = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/'

NGROK_URL = 'https://0782-83-10-33-25.ngrok-free.app'  # Zmiana na aktualny link ngrok

# Ustawienie webhooka dla bota Telegram
def set_webhook():
    url = TELEGRAM_API_URL + 'setWebhook'
    payload = {'url': NGROK_URL + '/telegram-webhook'}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=payload, headers=headers)
    print(response.json())

# Obsługa webhooka Telegram
@app.route('/telegram-webhook', methods=['POST'])
def telegram_webhook():
    data = request.json
    logging.debug('Received update: %s', data)
    if 'message' in data:
        chat_id = data['message']['chat']['id']
        message_text = data['message']['text']
        logging.debug('Chat ID: %s, Message Text: %s', chat_id, message_text)
        response_text = get_response(message_text)
        logging.debug('Response Text: %s', response_text)
        send_message(chat_id, response_text)
    return 'OK', 200

# Funkcja do wysyłania wiadomości do użytkownika Telegram
def send_message(chat_id, text):
    url = TELEGRAM_API_URL + 'sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=payload, headers=headers)
    logging.debug('Send message response: %s', response.json())

# Uruchomienie aplikacji
if __name__ == "__main__":
    set_webhook()  # Ustawienie za każdym razem gdy zmienia się link ngrok
    app.run(port=5000, debug=True)
