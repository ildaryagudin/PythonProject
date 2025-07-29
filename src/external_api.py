import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('EXCHANGE_RATES_API_KEY')
BASE_URL = f'https://api.apilayer.com/exchangerates_data/latest'
HEADERS = {
    'apikey': API_KEY,
}


def convert_to_rubles(amount: float, currency: str) -> float:
    response = requests.get(BASE_URL, headers=HEADERS, params={'base': currency})
    if response.status_code != 200:
        raise Exception("Ошибка при получении курсов валют.")

    rates = response.json().get('rates', {})
    rub_rate = rates.get('RUB', None)
    if rub_rate is None:
        raise ValueError(f"Валюта RUB отсутствует в результатах обмена ({currency}).")

    return amount * rub_rate


# external_api.py
def transaction_amount_in_rubles(transaction: dict) -> float:
    amount = transaction['amount']
    currency = transaction['currency'].upper()  # Используем верхний регистр для сопоставимости

    if currency == 'RUB':
        return amount
    elif currency in ['USD', 'EUR']:
        return convert_to_rubles(amount, currency)
    else:
        raise ValueError(f"Невозможно обработать валюту '{currency}'")