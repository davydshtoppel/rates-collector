from django.views import View
from django.http import JsonResponse

import logging
import json

from .mappers import rates_to_json, currencies_to_json
from .models import Currency, Rate


logger = logging.getLogger(__name__)


class CurrencyCache:
    def __init__(self):
        self.currencies = {}

    def get_currency(self, currency_name) -> Currency:
        currency = self.currencies.get(currency_name, None)
        if currency:
            return currency
        currency, created = Currency.objects.get_or_create(name=currency_name)
        self.currencies[currency_name] = currency
        return currency


currency_cache = CurrencyCache()


class DailyRatesView(View):

    def put(self, request, day):
        logger.info("Request body: %s", request.body)
        body = json.loads(request.body)
        Rate.objects.filter(date=day).delete()
        for base_rates in body['rates']:
            base = base_rates['base']
            base = currency_cache.get_currency(base)
            for single_rate in base_rates['values']:
                currency = single_rate['currency']
                rate = single_rate['rate']
                currency = currency_cache.get_currency(currency)
                Rate.objects.create(base=base, currency=currency, date=day, value=rate)
        return JsonResponse({})

    def delete(self, request, day):
        Rate.objects.filter(date=day).delete()
        return JsonResponse({})

    def patch(self, request, day):
        logger.info("Request body: %s", request.body)
        body = json.loads(request.body)
        for base_rates in body['rates']:
            base = base_rates['base']
            base = currency_cache.get_currency(base)
            Rate.objects.filter(date=day, base=base).delete()
            for single_rate in base_rates['values']:
                currency = single_rate['currency']
                rate = single_rate['rate']
                currency = currency_cache.get_currency(currency)
                Rate.objects.create(base=base, currency=currency, date=day, value=rate)
        return JsonResponse({})

    def get(self, request, day):
        base = request.GET.get('base', default=None)
        if base:
            base = currency_cache.get_currency(base)
            rates = Rate.objects.filter(date=day, base=base).all()
        else:
            rates = Rate.objects.filter(date=day).all()
        if rates:
            return JsonResponse(rates_to_json(day, rates))
        return JsonResponse({}, status=404)


class LatestRatesView(View):

    def get(self, request):
        base = request.GET.get('base', default=None)
        currency = request.GET.get('currency', default=None)
        logger.info('Request for latest rates: base=[%s], currency=[%s]', base, currency)
        if base and currency:
            base = currency_cache.get_currency(base)
            currency = currency_cache.get_currency(currency)
            rates = Rate.objects.raw('SELECT * FROM rates_rate'
                                     ' WHERE date=(SELECT MAX(date) FROM rates_rate)'
                                     ' AND base_id=%s'
                                     ' AND currency_id=%s',
                                     [base.id, currency.id])
        elif currency:
            currency = currency_cache.get_currency(currency)
            rates = Rate.objects.raw('SELECT * FROM rates_rate'
                                     ' WHERE date=(SELECT MAX(date) FROM rates_rate)'
                                     ' AND currency_id=%s',
                                     [currency.id])
        elif base:
            base = currency_cache.get_currency(base)
            rates = Rate.objects.raw('SELECT * FROM rates_rate'
                                     ' WHERE date=(SELECT MAX(date) FROM rates_rate)'
                                     ' AND base_id=%s',
                                     [base.id])
        else:
            rates = Rate.objects.raw('SELECT * FROM rates_rate WHERE date=(SELECT MAX(date) FROM rates_rate)')
        if not rates or not rates[0].id:
            return JsonResponse({}, status=404)
        logger.info('Response: day: %s, rates: %s', rates[0].date, rates)
        return JsonResponse(rates_to_json(rates[0].date, rates))


class CurrenciesView(View):
    def get(self, request):
        return JsonResponse(currencies_to_json(Currency.objects.all()))
