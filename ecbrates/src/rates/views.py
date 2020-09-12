from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse

import json, logging

from .models import Currency, Rate


logger = logging.getLogger(__name__)


class RatesView(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.currencies = dict(map(lambda x: (x.name, x), Currency.objects.all()))

    def get_or_create_currency(self, currency_name: str) -> Currency:
        currency = self.currencies.get(currency_name, None)
        if not currency:
            currency = Currency.objects.create(name=currency_name)
            self.currencies[currency_name] = currency
        return currency

    def put(self, request, day):
        print(request.body)
        body = json.loads(request.body)
        Rate.objects.filter(date=day).delete()
        for base_rates in body['rates']:
            base = base_rates['base']
            base = self.get_or_create_currency(base)
            for single_rate in base_rates['values']:
                currency = single_rate['currency']
                rate = single_rate['rate']
                currency = self.get_or_create_currency(currency)
                Rate.objects.create(base_id=base, currency_id=currency, date=day, value=rate)
        return JsonResponse({})

    def get(self, request, day):
        rates = Rate.objects.filter(date=day).all()
        by_base = {}
        for rate in rates:
            base = rate.base_id.name
            base_values = by_base.get(base, [])
            base_values.append({'currency': rate.currency_id.name, 'rate': rate.value})
            by_base[base] = base_values
        result = []
        for base, values in by_base.items():
            result.append({'base': base, 'values': values})
        return JsonResponse({'rates': result})
