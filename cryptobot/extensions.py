import requests
import json
from config import keys

class APIException(Exception):
    pass


class Currency:

    @staticmethod
    def get_price(message):
        values = message.split(' ')
        if len(values) != 3:
            raise APIException('Неверное количество параметров.')

        base, quote, amount = values
        base, quote = base.lower(), quote.lower()


        if quote.lower() == base.lower():
            raise APIException(f'Невозможно перевести одинаковые валюты {base}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')


        r = requests.get(f"https://api.exchangeratesapi.io/latest?base={base_ticker}")
        price = json.loads(r.content)['rates'][quote_ticker]
        result = round(float(price) * float(amount), 2)
        text = f'Цена {amount} {base} в {quote} - {result}'
        return text