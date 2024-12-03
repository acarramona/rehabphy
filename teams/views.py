# teams/views
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Group
from accounts.forms import PatientSignUpForm, PhysioSignUpForm
from accounts.models import User
from accounts.services import send_invitation_email, send_registration_email
from patients.models import Patient
from physios.models import Physio
from teams.forms import InviteForm
from django.contrib import messages
import logging

logger: logging.Logger = logging.getLogger('teams')

def is_team(user):
    if user.is_authenticated and user.groups.filter(name='PHYSIO_TEAM').exists():
        return True
    else:
        raise PermissionDenied('Access restricted to Physio Teams.')

@login_required
@user_passes_test(is_team)
def team_dashboard(request):    
    # Fetch the data for registered patients and physios
    patients = Patient.objects.all()
    physios = Physio.objects.all()
    patient_count: int = patients.count()
    physio_count: int = physios.count()

    context = {
        'patients': patients,
        'physios': physios,
        'physio_count': physio_count,
        'patient_count': patient_count,
    }
    return render(request, 'teams/team_dashboard.html', context)



@login_required
@user_passes_test(is_team)
def email_invite(request):
    if request.method == 'POST':
        form = InviteForm(request.POST)
        if form.is_valid():
            target = form.cleaned_data['target']
            emails = form.extract_emails()
            try:
                # Assuming send_invitation_email returns True on success
                if target == "physio":
                    success: bool = send_invitation_email(request, emails, is_physio=True)
                else:
                    success = send_invitation_email(request, emails, is_physio=False)

                if success:
                    messages.success(request, "Invitations have been sent successfully.")
                    return redirect('teams:email_invite')
                else:
                    messages.error(request, "An error occurred while sending invitations.")
            except Exception as e:
                # Log the exception and show an error message
                print(f"Error sending invitations: {e}")
                messages.error(request, "An unexpected error occurred. Please try again.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = InviteForm()
    
    return render(request, 'teams/send_invite.html', {'form': form})

@login_required
@user_passes_test(is_team)
def register_physio(request):
    if request.method == 'POST':
        form = PhysioSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Add user to PHYSIO group
            group, created = Group.objects.get_or_create(name='PHYSIO')
            user.groups.add(group)

            try:
                # send_registration_email returns True on success
                success: bool = send_registration_email(
                    request, user.physio.get_full_name(), user.email, form.generated_password
                )

                if success:
                    messages.success(request, "Physiotherapist account created. Account details is sent to their email.")
                    return redirect('teams:register_physio')
                else:
                    messages.error(request, "An error occurred while creating account.")
            except Exception as e:
                print(e)
                messages.error(request, "An unexpected error occurred. Please try again.")
    else:
        form = PhysioSignUpForm()
    return render(request, 'teams/physio_signup.html', {'form': form})

@login_required
@user_passes_test(is_team)
def register_patient(request):
    if request.method == 'POST':
        form = PatientSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Add user to PATIENT group
            group, created = Group.objects.get_or_create(name='PATIENT')
            user.groups.add(group)

            try:
                # send_registration_email returns True on success
                success: bool = send_registration_email(
                    request, user.patient.get_full_name(), user.email, form.generated_password
                )

                if success:
                    messages.success(request, "Patient account created. Account details is sent to their email.")
                    return redirect('teams:register_patient')
                else:
                    messages.error(request, "An error occurred while creating account.")
            except Exception as e:
                print(e)
                messages.error(request, "An unexpected error occurred. Please try again.")
    else:
        form = PatientSignUpForm()
    return render(request, 'teams/patient_signup.html', {'form': form})