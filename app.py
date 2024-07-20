from flask import Flask, render_template, request, jsonify
from chatbot import get_response
from bot_utils import log_conversation

app = Flask(__name__)

# Lista przechowująca historię rozmowy
conversation = []

# Obsługa żądania GET dla strony głównej
@app.get("/")
def index_get():
    return render_template('index.html')

# Obsługa żądania POST dla przewidywania odpowiedzi
@app.post("/predict")
def predict():
    # Pobranie wiadomości z żądania
    text = request.get_json().get('message')
    # Uzyskanie odpowiedzi z chatbot
    response = get_response(text)
    # Dodanie wiadomości i odpowiedzi do historii rozmowy
    conversation.append((text, response))
    message = {"answer": response}
    return jsonify(message)

# Obsługa żądania POST dla logowania rozmów
@app.route("/log", methods=["POST"])
def log():
    log_conversation(conversation)
    conversation.clear()
    return jsonify({"status": "success"})

# Uruchomienie aplikacji
if __name__ == "__main__":
    app.run(port=8080, debug=True)
