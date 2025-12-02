# mapapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('USA.json', views.get_USAJSON, name='get_USAJSON'),
]