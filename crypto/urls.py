from django.conf.urls import include, url
from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'crypto'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index')
]
