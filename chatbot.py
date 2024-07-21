import random
import json
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize, detect_language
from bot_utils import remove_polish_diacritics, buy_calculator, sell_calculator, countries_currency, currency_country, rate_question, check_availability, log_conversation

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('exchange-intents.json', 'r', encoding='utf-8') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

intent_to_function = {
    "kursy": rate_question,
    "exchange_rate": rate_question,
    "kraj_waluta": countries_currency,
    "country_currency": countries_currency,
    "waluta_kraj": currency_country,
    "currency_country": currency_country,
    "kupno": buy_calculator,
    "buy_currency": buy_calculator,
    "sprzedaz": sell_calculator,
    "sell_currency": sell_calculator,
    "dostepnosc": check_availability,
    "availability": check_availability
}

bot_name = "Cash"

def get_response(msg):
    language = detect_language(msg)
    if language == 'polish':
        msg = remove_polish_diacritics(msg)
    sentence = tokenize(msg, language=language)
    X = bag_of_words(sentence, all_words, language=language)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.90:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                if tag in intent_to_function:
                    return intent_to_function[tag](sentence, language)
                else:
                    return random.choice(intent['responses'])

    # Fallback response if the intent is not confidently identified
    return "Nie rozumiem..." if language == 'polish' else "I don't understand..."

if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")
    conversation = []
    while True:
        sentence = input("You: ")
        if sentence == "quit":
            break

        resp = get_response(sentence)
        conversation.append((sentence, resp))
        print(resp)

    log_conversation(conversation)
