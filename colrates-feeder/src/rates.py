from datetime import datetime, date

import requests
import json


class Rate:
    def __init__(self, currency: str, value: float):
        self.currency = currency
        self.value = value

    def __str__(self):
        return f'({self.currency}: {self.value})'

    def __repr__(self):
        return self.__str__()


class DailyRates:
    def __init__(self, day: date):
        self.date = day
        self.rates = []

    def __str__(self):
        return f'(date={self.date}, rates={self.rates})'

    def __repr__(self):
        return self.__str__()


class RatesCollectorException(Exception):
    def __init__(self, response):
        self.message = f'Error from Rates Collector. Status code: {response.status_code},' \
                       f' response body: {response.content}'

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.message


class RatesCollector:
    def __init__(self, url):
        self.url = url

    def last_update(self, base: str):
        response = requests.get(f'{self.url}/rates/api/latest/?base={base}')
        if response.status_code == 200:
            rates = json.loads(response.content)
            return datetime.strptime(rates['date'], '%Y-%m-%d').date()
        elif response.status_code != 404:
            raise RatesCollectorException(response)
        return None

    def update_rates(self, base: str, daily_rates: DailyRates):
        day = daily_rates.date.strftime('%Y-%m-%d')
        rates = [{'currency': x.currency, 'rate': x.value} for x in daily_rates.rates]
        body = {'rates': [{'base': base, 'values': rates}]}
        response = requests.patch(f'{self.url}/rates/api/{day}/', json.dumps(body))
        if response.status_code != 200:
            raise RatesCollectorException(response)
