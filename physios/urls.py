# physios/urls.py

from django.urls import path, include
from django.urls.resolvers import URLPattern
from . import views

app_name = 'physios' 

urlpatterns = [
    path('dashboard/', views.physio_dashboard, name='dashboard'),
]