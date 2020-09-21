from django.urls import path, register_converter

from .converters import DateConverter
from .views import RatesView, LatestRatesView


register_converter(DateConverter, 'yyyy-mm-dd')

urlpatterns = [
    path('<yyyy-mm-dd:day>/', RatesView.as_view()),
    path('latest/', LatestRatesView.as_view()),
]