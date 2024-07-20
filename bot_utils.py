import requests
import unicodedata
import csv
import json
from dotenv import load_dotenv
from datetime import datetime
import os

# Załadowanie konfiguracji z pliku .env
load_dotenv('.config')
api_key = os.getenv('API_KEY')

# Lista obsługiwanych walut
currencies = ["USD", "EUR", "GBP", "CHF", "SEK", "NOK", "DKK", "CAD", "AUD", "CZK", "HUF", "JPY", "ALL", "RON", "RUB", "CNY", "BGN", "UAH", "ILS", "TRY", "GEL", "KRW", "EGP", "AED"]

# Mapowanie krajów na waluty i odwrotnie
country_to_currency_pl = {}
currency_to_country_pl = {}
currency_names_pl = {}
all_currencies_pl = []

country_to_currency_eng= {}
currency_to_country_eng= {}
currency_names_eng = {}
all_currencies_eng = []

# Załadowanie danych krajów i walut z pliku CSV
with open('./misc/countries_currencies_pl.csv', mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        country = row['country']
        currency = row['currency']
        code = row['code']
        country_to_currency_pl[country] = code
        currency_to_country_pl[code] = country
        currency_names_pl[code] = currency
        all_currencies_pl.append(code)
        
with open('./misc/countries_currencies_eng.csv', mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        country = row['country']
        currency = row['currency']
        code = row['code']
        country_to_currency_eng[country] = code
        currency_to_country_eng[code] = country
        currency_names_eng[code] = currency
        all_currencies_eng.append(code)

# Załadowanie dostępnych walut z pliku JSON
with open('./misc/available_currencies.json', 'r', encoding='utf-8') as json_data:
    available_currencies = json.load(json_data)

# Funkcja usuwająca polskie znaki diakrytyczne
def remove_polish_diacritics(text):
    return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )

# Funkcja pobierająca kurs wymiany waluty
def fetch_exchange_rate(currency):
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{currency}/PLN"
    response = requests.get(url)
    data = response.json()
    rate = data['conversion_rate']
    return rate

# Funkcja odpowiadająca na pytanie o kurs waluty
def rate_question(sentence, language):
    for word in sentence:
        if word.upper() in currencies:
            currency = word.upper()
            rate = fetch_exchange_rate(currency)
            sell_rate = rate * 1.015
            buy_rate = rate * 0.995
            if rate:
                if language == 'polish':
                    return f"Aktualny kurs {currency} to:\nKupno {buy_rate:.4f} PLN,\nSprzedaż {sell_rate:.4f} PLN."
                else:
                    return f"The current rate for {currency} is:\nBuy {buy_rate:.4f} PLN,\nSell {sell_rate:.4f} PLN."
            else:
                if language == 'polish':
                    return f"Nie mogłem znaleźć kursu dla {currency}."
                else:
                    return f"Couldn't find the rate for {currency}."
    if language == 'polish':
        return "Niestety nie sprzedajemy tej waluty."
    else:
        return "Unfortunately, we do not sell this currency."

# Funkcja odpowiadająca na pytanie o walutę kraju
def countries_currency(sentence, language):
    for word in sentence:
        country = word.title()
        if country in country_to_currency_pl or country in country_to_currency_eng:
            if language == 'polish':
                currency_code = country_to_currency_pl[country]
                currency_name = currency_names_pl[currency_code]
                return f"Waluta używana w {country} to {currency_name} ({currency_code})."
            else:
                currency_code = country_to_currency_eng[country]
                currency_name = currency_names_eng[currency_code]
                return f"The currency used in {country} is {currency_name} ({currency_code})."
    if language == 'polish':
        return "Nie mogłem znaleźć informacji o tej walucie."
    else:
        return "Couldn't find information about this currency."

# Funkcja odpowiadająca na pytanie o kraj używający danej waluty
def currency_country(sentence, language):
    for word in sentence:
        if word.upper() in currency_to_country_pl or word.upper() in currency_to_country_eng:
            if word.upper() == 'EUR':
                if language == 'polish':
                    return "Waluta Euro (EUR) jest używana w wielu krajach europejskich, takich jak Niemcy, Francja czy Włochy."
                else:
                    return "The Euro (EUR) is used in many European countries, such as Germany, France, and Italy."
            else:
                if language == 'polish':
                    country = currency_to_country_pl[word.upper()]
                    currency_name = currency_names_pl[word.upper()]
                    return f"Kraj używający waluty {currency_name} ({word.upper()}) to {country}."
                else:
                    country = currency_to_country_eng[word.upper()]
                    currency_name = currency_names_eng[word.upper()]
                    return f"The country using {currency_name} ({word.upper()}) is {country}."
    if language == 'polish':
        return "Nie mogłem znaleźć informacji o tej walucie."
    else:
        return "Couldn't find information about this currency."

# Funkcja sprawdzająca zdanie pod kątem waluty i kwoty
def check_sentence_for_currency(sentence, language):
    currency = None
    amount = 0
    for word in sentence:
        if word.upper() in available_currencies:
            currency = word.upper()
        try:
            amount = float(word)
        except ValueError:
            continue
    
    if not currency or amount <= 0:
        if language == 'polish':
            return None, None, "Proszę podać prawidłową walutę i kwotę. Użyj właściwego kodu waluty i pamiętaj o przerwie między kwotą a kodem."
        else:
            return None, None, "Please provide a valid currency and amount. Use the correct currency code and remember to separate the amount and the code."
    
    return currency, amount, None

# Funkcja kalkulująca koszt kupna waluty
def buy_calculator(sentence, language):
    currency, amount, error = check_sentence_for_currency(sentence, language)
    if error:
        return error
    
    rate = fetch_exchange_rate(currency)
    rate = rate * 1.015
    cost = amount * rate
    
    if language == 'polish':
        return f"Za {amount:.2f} {currency} musisz zapłacić {cost:.2f} PLN."
    else:
        return f"To buy {amount:.2f} {currency}, you need to pay {cost:.2f} PLN."

# Funkcja kalkulująca dochód ze sprzedaży waluty
def sell_calculator(sentence, language):
    currency, amount, error = check_sentence_for_currency(sentence, language)
    if error:
        return error

    rate = fetch_exchange_rate(currency)
    rate = rate * 0.995
    proceeds = amount * rate
    
    if language == 'polish':
        return f"Sprzedając {amount:.2f} {currency} otrzymasz {proceeds:.2f} PLN."
    else:
        return f"By selling {amount:.2f} {currency}, you will receive {proceeds:.2f} PLN."

# Funkcja sprawdzająca dostępność waluty
def check_availability(sentence, language):
    currency, amount, error = check_sentence_for_currency(sentence, language)
    if error:
        return error
    
    available_amount = available_currencies.get(currency, 0)
    
    if available_amount < amount:
        if language == 'polish':
            return f"Niestety nie mamy {amount:.2f} {currency}."
        else:
            return f"Unfortunately, we do not have {amount:.2f} {currency}."
    else:
        if language == 'polish':
            return f"Mamy wystarczającą kwotę by sprzedać {amount:.2f} {currency}."
        else:
            return f"We have enough to sell you {amount:.2f} {currency}."

# Funkcja logująca historię rozmów
def log_conversation(conversation):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join('conv_logs', f"conversation_{timestamp}.txt")
    with open(filename, 'w', encoding='utf-8') as file:
        for message, response in conversation:
            if response == "Nie rozumiem..." or response == "I don't understand...":
                file.write(f"User: {message} [-!--------------problematic--------------!-]\n")
            else:
                file.write(f"User: {message}\n")
            file.write(f"Bot: {response}\n\n")
