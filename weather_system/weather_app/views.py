import json
import pandas as pd
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
    data = {'code': 'ok', 'data': dict(Province.objects.values_list('province_name', 'province_id'))}
    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})


def get_weather_data(city_id, date):
    weahter_data = WeatherData.objects.filter(city_id=city_id, date=date)[0]
    if weahter_data:
        return {"city_id": weahter_data.city_id, "date": weahter_data.date, "temperature": weahter_data.temperature,
                "precipitation": weahter_data.precipitation, "wind_speed": weahter_data.wind_speed,
                "wind_direction": weahter_data.wind_direction, "air_pressure": weahter_data.air_pressure,
                "humidity": weahter_data.humidity, "cloud_cover": weahter_data.cloud_cover}
    return None


def get_date(request):
    date = {'code': 'ok', 'data': [item for item in WeatherData.objects.values('date').distinct()]}
    return JsonResponse(date, safe=False, json_dumps_params={'ensure_ascii': False})


def get_province_weather(request):
    weather_data_city = list()
    province = request.GET.get('province', None)
    date = request.GET.get('date', None)
    if province is not None and date is not None:
        city = City.objects.filter(province_id=province)
        for item in city:
            weather_data_city.append(get_weather_data(item.city_id, date))

        df = pd.DataFrame(weather_data_city)
        weather_data_province = {'name': Province.objects.filter(province_id=province)[0].province_name, 'date': date,
                                 'value': df['temperature'].mean(), 'precipitation': df['precipitation'].mean(),
                                 'wind_speed': df['wind_speed'].mean(), 'air_pressure': df['air_pressure'].mean(),
                                 'humidity': df['humidity'].mean(), 'cloud_cover': df['cloud_cover'].mean()}

        return JsonResponse({"cody": "ok", "data": weather_data_province}, json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({"cody": "error", "data": None})


def get_ChinaJSON(request):
    China_json = os.path.join(settings.BASE_DIR, 'weather_app/static/geojson/中华人民共和国_省.geojson')
    with open(China_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return JsonResponse(data)


def max_temperature(request):
    return JsonResponse({'code': 'ok', 'data': max(WeatherData.objects.values_list('temperature'))})


def min_temperature(request):
    return JsonResponse({'code': 'ok', 'data': min(WeatherData.objects.values_list('temperature'))})
