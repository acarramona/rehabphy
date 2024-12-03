from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings

def send_registration_email(request, name, recipient_email, password):
    subject = 'Welcome to Our Service!'
    
    # Construct the login URL
    login_url = request.build_absolute_uri(reverse('accounts:login'))
    
    # Prepare the email content
    html_message = render_to_string('emails/welcome_email.html', {
        'name': name,
        'username': recipient_email,
        'password': password,
        'login_url': login_url,
    })
    plain_message = strip_tags(html_message)

    try:
        # Send the email
        send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [recipient_email], html_message=html_message)
        return True
    except Exception as ex:
        raise Exception(ex)
    

def send_invitation_email(request, recipients, is_physio=False):
    url = request.build_absolute_uri(reverse('home'))
    context = {
        'company_name': 'Rehabphy',
        'contact_email': 'info@rehabphy.com',
        'sender_name': request.user.physioteam.get_full_name(),
        'sender_title': 'Physiotherapist Team',
        'url': url,
    }

    if is_physio:
        subject = 'Invitation to Join Our Physiotherapy Team'
        template = 'emails/invite_physio_email.html'
    else:
        subject = 'Invitation to Join Our Physiotherapy Services'
        template = 'emails/invite_patient_email.html'
    html_content = render_to_string(template, context)
    plain_message = strip_tags(html_content)

    try:
        # Send the email
        for recipient in recipients:
            send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [recipient], html_message=html_content)
        return True
    except Exception as ex:
        raise Exception(ex)