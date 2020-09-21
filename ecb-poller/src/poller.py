from xml.etree import ElementTree
from datetime import datetime, date

import requests
import json
import os


class Rate:
    def __init__(self, currency: str, value: float):
        self.currency = currency
        self.value = value

    def __str__(self):
        return f'({self.currency}: {self.value})'

    def __repr__(self):
        return self.__str__()


class DailyRates:
    def __init__(self, date: date):
        self.date = date
        self.rates = []

    def __str__(self):
        return f'(date={self.date}, rates={self.rates})'

    def __repr__(self):
        return self.__str__()


class EcbServer:
    def __init__(self, ecb_url):
        self.ecb_url = ecb_url

    def parse_ecb_response(self, ecb_response):
        root = ElementTree.fromstring(ecb_response)
        daily_rates = root.findall(f"*/{{http://www.ecb.int/vocabulary/2002-08-01/eurofxref}}Cube/[@time]")
        result = []
        for daily_rate in daily_rates:
            value = DailyRates(datetime.strptime(daily_rate.attrib['time'], '%Y-%m-%d').date())
            for rate in daily_rate:
                value.rates.append(Rate(rate.attrib['currency'], rate.attrib['rate']))
            result.append(value)
        return result

    def daily_rates(self):
        response = requests.get(f'{self.ecb_url}/stats/eurofxref/eurofxref-daily.xml')
        return self.parse_ecb_response(response.content)[0]

    def history_rates(self):
        response = requests.get(f'{self.ecb_url}/stats/eurofxref/eurofxref-hist.xml')
        return self.parse_ecb_response(response.content)


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

    def last_update(self):
        response = requests.get(f'{self.url}/rates/api/latest/?base=EUR')
        if response.status_code == 200:
            rates = json.loads(response.content)
            return datetime.strptime(rates['date'], '%Y-%m-%d').date()
        elif response.status_code != 404:
            raise RatesCollectorException(response)
        return None

    def update_rates(self, daily_rates: DailyRates):
        day = daily_rates.date.strftime('%Y-%m-%d')
        rates = [{'currency': x.currency, 'rate': x.value} for x in daily_rates.rates]
        body = {'rates': [{'base': 'EUR', 'values': rates}]}
        response = requests.put(f'{self.url}/rates/api/{day}/', json.dumps(body))
        if response.status_code != 200:
            raise RatesCollectorException(response)


rc_url = os.getenv('RATES_URL', 'http://localhost:8000')
ecb = EcbServer('https://www.ecb.europa.eu')
rc = RatesCollector(rc_url)

last_rates = rc.last_update()
if not last_rates:
    for it in ecb.history_rates():
        rc.update_rates(it)
else:
    current_date = datetime.now().date()
    if last_rates != current_date:
        ecb_last_rates = ecb.daily_rates()
        if ecb_last_rates.date != last_rates:
            rc.update_rates(ecb_last_rates)
