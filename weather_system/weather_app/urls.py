# mapapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('USA.json', views.get_USAJSON, name='get_USAJSON'),
    path('china.json', views.get_ChinaJSON, name='get_ChinaJSON'),
    path('province_weather', views.get_province_weather, name='get_province_weather'),
    path('province_ID', views.get_province_ID, name='get_province_ID'),
    path('get_date', views.get_date, name='get_date'),
]