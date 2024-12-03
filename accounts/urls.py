# accounts/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from accounts.forms import CustomAuthenticationForm
from . import views

app_name = 'accounts'

urlpatterns = [
    # Login and Logout URLs
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='accounts/login.html',
            authentication_form=CustomAuthenticationForm
        ),
        name='login'
    ),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Password Reset URLs
    path('reset-password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset-password/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Redirect After Login
    path('redirect/', views.redirect_after_login, name='redirect_after_login'),

    # User Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Sign-up URLs
    path('signup/patient/', views.patient_signup, name='patient_signup'),
    path('signup/physio/', views.physio_signup, name='physio_signup'),
    path('signup/physio-team/', views.physio_team_signup, name='physio_team_signup'),
]

