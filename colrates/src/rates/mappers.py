from datetime import date


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


def currencies_to_json(currencies: []) -> dict:
    return {'currencies': [it.name for it in currencies]}
