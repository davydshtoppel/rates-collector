from datetime import date, datetime


class DateConverter:
    regex = '\\d{4}-\\d{2}-\\d{2}'

    def to_python(self, value: str) -> date:
        return datetime.strptime(value, '%Y-%m-%d').date()

    def to_url(self, value: date):
        return value.strftime('%Y-%m-%d')
