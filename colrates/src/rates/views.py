from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

from datetime import date
import logging
import json

from .models import Currency, Rate


logger = logging.getLogger(__name__)


def rates_to_json(day: date, rates: []) -> dict:
    by_base = {}
    for rate in rates:
        base = rate.base.name
        base_values = by_base.get(base, [])
        base_values.append({'currency': rate.currency.name, 'rate': rate.value})
        by_base[base] = base_values
    result = []
    for base, values in by_base.items():
        result.append({'base': base, 'values': values})
    return {'rates': result, 'date': day.strftime('%Y-%m-%d')}


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
        if base:
            base = currency_cache.get_currency(base)
            query_set = Rate.objects.raw('SELECT * FROM rates_rate WHERE base_id=%s ORDER BY date DESC LIMIT 1',
                                         [base.id])
        else:
            query_set = Rate.objects.raw('SELECT * FROM rates_rate ORDER BY date DESC LIMIT 1')
        if not query_set or not query_set[0].id:
            return JsonResponse({}, status=404)
        latest_rate = query_set[0]
        day = latest_rate.date
        if not base:
            rates = Rate.objects.filter(date=latest_rate.date).all()
        else:
            rates = Rate.objects.filter(date=latest_rate.date, base=base).all()
        logger.info('Response: day: %s, rates: %s', day, rates)
        return JsonResponse(rates_to_json(day, rates))
