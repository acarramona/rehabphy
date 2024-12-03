# patients/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('schedule/', views.schedule_therapy_session, name='schedule_therapy_session'),
    path('assessments/', views.patient_assessments, name='assessments'),
]
