from xml.etree import ElementTree
from datetime import datetime

from rates import Rate, DailyRates

import requests


class EcbServer:

    @staticmethod
    def parse_ecb_response(ecb_response):
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
        response = requests.get('https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml')
        return self.parse_ecb_response(response.content)[0]

    def history_rates(self):
        response = requests.get('https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.xml')
        return self.parse_ecb_response(response.content)
