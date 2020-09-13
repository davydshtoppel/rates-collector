from django.urls import path, register_converter

from .converters import DateConverter
from .views import RatesView


register_converter(DateConverter, 'yyyy-mm-dd')

urlpatterns = [
    path('<yyyy-mm-dd:day>/', RatesView.as_view()),
]