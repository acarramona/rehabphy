# accounts/views

from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth import views as auth_views
from accounts.forms import PatientSignUpForm, PhysioSignUpForm, PhysioTeamSignUpForm
from accounts.models import User
from accounts.services import send_registration_email
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.urls import reverse

# Password reset view using Django auth views
reset_password_view = auth_views.PasswordResetView.as_view(template_name='accounts/reset_password.html')

def patient_signup(request):
    if request.method == 'POST':
        form = PatientSignUpForm(request.POST)
        if form.is_valid():
            user: User = form.save()
            # Add user to the "PATIENT" group
            group, created = Group.objects.get_or_create(name='PATIENT')
            user.groups.add(group)

            try:
                # send_registration_email returns True on success
                success: bool = send_registration_email(
                        request, user.patient.get_full_name(), user.email, form.cleaned_data.get('password1')
                )

                if success:
                    messages.success(request, "Your account details have been sent to your email.")
                    login(request, user)
                    return redirect('patients:patient_dashboard')
                else:
                    messages.error(request, "An error occurred while sending the registration email.")
            except Exception as e:
                # Log the exception and show an error message
                messages.error(request, "An unexpected error occurred. Please try again.")
    else:
        form = PatientSignUpForm()

    return render(request, 'accounts/patient_signup.html', {'form': form})

def physio_signup(request):
    if request.method == 'POST':
        form = PhysioSignUpForm(request.POST)
        if form.is_valid():
            user: User = form.save()
            # Add user to the "PHYSIO" group
            group, created = Group.objects.get_or_create(name='PHYSIO')
            user.groups.add(group)

            try:
                # send_registration_email returns True on success
                success: bool = send_registration_email(
                        request, user.physio.get_full_name(), user.email, form.cleaned_data.get('password1')
                )

                if success:
                    messages.success(request, "Your account details have been sent to your email.")
                    login(request, user)
                    return redirect('physios:dashboard')
                else:
                    messages.error(request, "An error occurred while sending the registration email.")
            except Exception as e:
                # Log the exception and show an error message
                messages.error(request, "An unexpected error occurred. Please try again.")
    else:
        form = PhysioSignUpForm()

    return render(request, 'accounts/physio_signup.html', {'form': form})

def physio_team_signup(request):
    if request.method == 'POST':
        form = PhysioTeamSignUpForm(request.POST)
        if form.is_valid():
            user: User = form.save()
            # Add user to the "PHYSIO_TEAM" group
            group, created = Group.objects.get_or_create(name='PHYSIO_TEAM')
            user.groups.add(group)

            try:
                # Retrieve the password from cleaned_data
                password = form.cleaned_data.get('password1')

                # send_registration_email returns True on success
                success: bool = send_registration_email(request, user.physioteam.get_full_name(), user.email, password)

                if success:
                    messages.success(request, "Your account details have been sent to your email.")
                    login(request, user)
                    return redirect('teams:dashboard')
                else:
                    messages.error(request, "An error occurred while sending the registration email.")
            except Exception as e:
                # Log the exception and show an error message
                messages.error(request, "An unexpected error occurred. Please try again.")
                print(e)
    else:
        form = PhysioTeamSignUpForm()

    return render(request, 'accounts/physio_team_signup.html', {'form': form})

@login_required
def redirect_after_login(request):
    """
    Redirect users after login based on their role or group membership.
    """
    user = request.user

    # Determine user role and redirect accordingly
    if user.groups.filter(name='PHYSIO_TEAM').exists():
        # Redirect to Physiotherapy Team Dashboard
        redirect_url = reverse('teams:dashboard')  
    elif user.groups.filter(name='PHYSIO').exists():
        # Redirect to Physio Dashboard
        redirect_url = reverse('physios:dashboard')  
    elif user.groups.filter(name='PATIENT').exists():
        # Redirect to Patient Dashboard
        redirect_url = reverse('patients:patient_dashboard')  
    else:
        # If no recognized group, raise a permission error
        raise PermissionDenied("User role not recognized.")

    return redirect(redirect_url)

@login_required
def dashboard(request):
    """
    Display the user's dashboard.
    """
    return render(request, 'accounts/dashboard.html')
