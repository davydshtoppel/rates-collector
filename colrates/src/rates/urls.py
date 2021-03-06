from django.urls import path, register_converter

from .converters import DateConverter
from .views import DailyRatesView, LatestRatesView, CurrenciesView


register_converter(DateConverter, 'yyyy-mm-dd')

urlpatterns = [
    path('<yyyy-mm-dd:day>/', DailyRatesView.as_view()),
    path('latest/', LatestRatesView.as_view()),
    path('currencies/', CurrenciesView.as_view()),
]
