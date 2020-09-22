from xml.etree import ElementTree
from datetime import datetime, date

from rates import Rate, DailyRates

import requests


class CbrServer:

    @staticmethod
    def parse_cbr_response(cbr_response):
        root = ElementTree.fromstring(cbr_response)
        day = datetime.strptime(root.attrib['Date'], '%d.%m.%Y').date()
        result = DailyRates(day)
        rates = root.findall("./Valute/[@ID]")
        for rate in rates:
            currency = None
            value = None
            nominal = None
            for el in rate:
                if el.tag == 'CharCode':
                    currency = el.text
                elif el.tag == 'Value':
                    value = el.text
                elif el.tag == 'Nominal':
                    nominal = el.text
            # 10 cron is 40 rub
            # 1 cron is 4 rub
            # 1 rub is 0.25 cron
            value_for_one = float(value.replace(',', '.')) / int(nominal)
            result.rates.append(Rate(currency, round(1 / value_for_one, 4)))
        return result

    def latest_rates(self):
        response = requests.get('https://www.cbr.ru/scripts/XML_daily_eng.asp')
        return self.parse_cbr_response(response.content)

    def daily_rates(self, day: date):
        response = requests.get(f"http://www.cbr.ru/scripts/XML_daily_eng.asp?date_req={day.strftime('%d/%m/%Y')}")
        return self.parse_cbr_response(response.content)
