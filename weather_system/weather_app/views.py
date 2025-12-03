import json
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
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


def get_province_weather(request):
    province = request.GET.get('province', None)

    if province is not None:
        city = City.objects.filter(province_id=province)
        print(city)
        return JsonResponse({"cody": "ok", "province": province})
    else:
        return JsonResponse({"cody": "ok", "province": None})


def get_ChinaJSON(request):
    China_json = os.path.join(settings.BASE_DIR, 'weather_app/static/geojson/中华人民共和国_省.geojson')
    with open(China_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return JsonResponse(data)


def get_china_geojson(request):
    geojson_path = os.path.join(settings.BASE_DIR, 'weather_system/static/geojson/中华人民共和国.geojson')
    with open(geojson_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return JsonResponse(data)
