import json

currencies = ["USD", "EUR", "GBP", "CHF", "SEK", "NOK", "DKK", "CAD", "AUD", "CZK", "HUF", "JPY", "ALL", "RON", "RUB", "CNY", "BGN", "UAH", "ILS", "TRY", "GEL", "KRW", "EGP", "AED"]

# Generate realistic stock levels based on currency value
currency_stock = {
    "USD": 20000,   # US Dollar
    "EUR": 18000,   # Euro
    "GBP": 15000,   # British Pound
    "CHF": 15000,   # Swiss Franc
    "SEK": 200000,  # Swedish Krona
    "NOK": 200000,  # Norwegian Krone
    "DKK": 150000,  # Danish Krone
    "CAD": 25000,   # Canadian Dollar
    "AUD": 25000,   # Australian Dollar
    "CZK": 400000,  # Czech Koruna
    "HUF": 5000000, # Hungarian Forint
    "JPY": 2000000, # Japanese Yen
    "ALL": 3000000, # Albanian Lek
    "RON": 400000,  # Romanian Leu
    "RUB": 5000000, # Russian Ruble
    "CNY": 150000,  # Chinese Yuan
    "BGN": 250000,  # Bulgarian Lev
    "UAH": 500000,  # Ukrainian Hryvnia
    "ILS": 50000,   # Israeli Shekel
    "TRY": 1000000, # Turkish Lira
    "GEL": 200000,  # Georgian Lari
    "KRW": 30000000,# South Korean Won
    "EGP": 1000000, # Egyptian Pound
    "AED": 100000   # UAE Dirham
}

with open('available_currencies.json', 'w') as f:
    json.dump(currency_stock, f)