#assessments/urls.py
from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

app_name = 'assessments'

urlpatterns = [
    path('patient/<int:patient_id>/create/', views.create_assessment, name='create_assessment'),
    path('assessment/<int:assessment_id>/', views.fetch_assessment, name='fetch_assessment'),
    path('patient/<int:patient_id>/assessments/<int:assessment_id>/', views.fetch_patient_assessment, name='fetch_patient_assessment'),
    path('patient/<int:patient_id>/assessments/', views.fetch_all_patient_assessments, name='fetch_all_patient_assessments'),
    path('physio/<int:physio_id>/assessments/', views.physio_assessments, name='physio_assessments'),
    path('all', views.fetch_all_assessments, name='fetch_all_assessments'),
    path('assessment/success/', views.assessment_success, name='assessment_success'),
]