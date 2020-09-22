import os
from datetime import datetime, date, timedelta

from cbr import CbrServer
from ecb import EcbServer
from rates import RatesCollector

rc_url = os.getenv('RATES_URL', 'http://localhost:8000')
rc = RatesCollector(rc_url)

current_date = datetime.now().date()

# Poll ECB
ecb = EcbServer()
last_rates = rc.last_update('EUR')
if not last_rates:
    for it in ecb.history_rates():
        rc.update_rates('EUR', it)
else:
    if last_rates != current_date:
        ecb_last_rates = ecb.daily_rates()
        if ecb_last_rates.date != last_rates:
            rc.update_rates('EUR', ecb_last_rates)


# Poll CBR
def date_generator(from_date, until_date):
    day = from_date
    while day <= until_date:
        yield day
        day += timedelta(days=1)


cbr = CbrServer()
last_rates = rc.last_update('RUB')
if not last_rates:
    last_rates = date(1999, 1, 1)

for it in date_generator(last_rates, current_date):
    # could return previous date
    rates = cbr.daily_rates(it)
    if rates.date == it:
        rc.update_rates('RUB', rates)
