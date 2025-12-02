import json
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import os

# Create your views here.
def index(request):
    return render(request, 'index.html')

def get_USAJSON(request):
    USA_json = os.path.join(settings.BASE_DIR, 'weather_app/static/geojson/USA.json')
    with open(USA_json, 'r') as f:
        data = json.load(f)
    return JsonResponse(data)

def get_china_geojson(request):
    """提供 china.json 的 API 接口（也可直接通过静态文件访问）"""
    geojson_path = os.path.join(settings.BASE_DIR, 'weather_system/static/geojson/中华人民共和国.geojson')
    with open(geojson_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return JsonResponse(data)