import json

from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.core import serializers
from .models import City, Province, WeatherData
import os


# Create your views here.
def index(request):
    return render(request, 'index.html')


def get_USAJSON(request):
    USA_json = os.path.join(settings.BASE_DIR, 'weather_app/static/geojson/USA.json')
    with open(USA_json, 'r') as f:
        data = json.load(f)
    return JsonResponse(data)


def get_province_ID(request):
    data = list(Province.objects.values_list('province_name', 'province_id'))
    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})


def get_weather_data(city_id, date):
    data = [[item.city_id, item.date, item.temperature, item.precipitation, item.wind_speed, item.wind_direction,
             item.air_pressure, item.humidity, item.cloud_cover] for item in
            WeatherData.objects.filter(city_id=city_id, date=date)]
    return data


def get_date(request):
    date = {'code': 'ok', 'data': [item for item in WeatherData.objects.values('date').distinct()]}

    return JsonResponse(date, safe=False, json_dumps_params={'ensure_ascii': False})


def get_province_weather(request):
    province = request.GET.get('province', None)
    date = request.GET.get('date', None)
    if province is not None and date is not None:
        city = City.objects.filter(province_id=province)
        weather_data = list()
        for item in city:
            weather_data.append(get_weather_data(item.city_id, date))
        return JsonResponse({"cody": "ok", "data": weather_data}, json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({"cody": "ok", "data": None})


def get_ChinaJSON(request):
    China_json = os.path.join(settings.BASE_DIR, 'weather_app/static/geojson/中华人民共和国_省.geojson')
    with open(China_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return JsonResponse(data)