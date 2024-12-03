# teams/urls.py

from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

app_name = 'teams'

urlpatterns: list[URLPattern] = [
    path('dashboard/', views.team_dashboard, name='dashboard'),
    path('invite/', views.email_invite, name='email_invite'),
    path('register/physio/', views.register_physio, name='register_physio'),
    path('register/patient/', views.register_patient, name='register_patient'),
]