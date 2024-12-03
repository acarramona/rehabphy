# views.py

# views.py

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.contrib.auth.forms import PasswordResetForm 

# Import User model
from accounts.models import User

# Import the functions to send emails from accounts.services
from accounts.services import send_invitation_email, send_registration_email

# Home view
def home(request):
    return render(request, 'index.html')

# Services view
def services(request):
    return render(request, 'services.html')

# Resources view
def resources(request):
    return render(request, 'resources.html')

# Contact view
def contact(request):
    return render(request, 'contact.html')

# Custom Permission Denied View (403)
def custom_permission_denied_view(request, exception=None):
    """
    Custom view to handle PermissionDenied exceptions and render the 403.html template,
    displaying the exception message.
    """
    if exception:
        message = str(exception)
    else:
        message = 'You do not have permission to access this page.'

    context = {
        'message': message
    }
    return render(request, '403.html', context, status=403)

# Custom Page Not Found View (404)
def custom_page_not_found_view(request, exception=None):
    """
    Custom view for handling 404 Page Not Found errors.
    """
    if exception:
        message = str(exception)
    else:
        message = 'The page you requested was not found.'

    context = {
        'message': message,
    }
    return render(request, '404.html', context, status=404)

# Custom Error View (500)
def custom_error_view(request, exception=None):
    """
    Custom view for handling 500 Internal Server errors.
    """
    if exception:
        message = str(exception)
    else:
        message = 'An internal server error occurred.'

    context = {
        'message': message,
    }
    return render(request, '500.html', context, status=500)

# Test View
@login_required
def test_view(request):
    """
    Test view to send an invitation email and check some user attributes.
    Requires user to be logged in.
    """
    user = request.user

    # Example email sending function call
    send_invitation_email(
        request,
        ['angelocarramona87@gmail.com', 'angelocarramona@hotmail.com'],
        is_important=True
    )

    return HttpResponse(f"User: {user.date_joined}, Authenticated: {user.physioteamprofile}")

# View to handle successful assessment (placeholder)
def assessment_success(request):
    """
    View for displaying a success message after assessment creation.
    """
    return render(request, 'assessments/assessment_success.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

def password_reset_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(request=request)
            return redirect('accounts:password_reset_done')
    else:
        form = PasswordResetForm()
    return render(request, 'accounts/password_reset.html', {'form': form})

def password_reset_done_view(request):
    return render(request, 'accounts/password_reset_done.html')