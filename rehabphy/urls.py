"""
URL configuration for rehabphy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Home page
    path('', views.home, name='home'),

    # Admin site
    path('admin/', admin.site.urls),

    # Accounts app
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),

    # Patients app
    path('patients/', include(('patients.urls', 'patients'), namespace='patients')),

    # Physios app
    path('physios/', include(('physios.urls', 'physios'), namespace='physios')),

    # Physioteams app
    path('physioteams/', include(('teams.urls', 'teams'), namespace='teams')),

    # Assessments app
    path('assessments/', include(('assessments.urls', 'assessments'), namespace='assessments')),

    # Services page
    path('services/', views.services, name='services'),

    # Resources page
    path('resources/', views.resources, name='resources'),

    # Contact page
    path('contact/', views.contact, name='contact'),

    # Assessment Success page
    path('assessments/success/', views.assessment_success, name='assessment_success'),

    # Dashboard 
    path('dashboard/', views.dashboard, name='dashboard'),

    # Password Reset Views (Correct the path according to your actual structure)
    path('accounts/password_reset/', views.password_reset_view, name='password_reset'),
    path('reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Test view
    path('test/', views.test_view, name='test_view'),
]

# Debug URLs for error handling during development
if settings.DEBUG:
    urlpatterns += [
        path('403/', views.custom_permission_denied_view, name='permission_denied'),
        path('404/', views.custom_page_not_found_view, name='page_not_found'),
        path('500/', views.custom_error_view, name='server_error'),
    ]

# Error handlers for production environment
handler403 = 'rehabphy.views.custom_permission_denied_view'
handler404 = 'rehabphy.views.custom_page_not_found_view'
handler500 = 'rehabphy.views.custom_error_view'
