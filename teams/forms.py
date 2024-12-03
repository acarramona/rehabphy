import re
import logging
from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

logger: logging.Logger = logging.getLogger('teams')

class InviteForm(forms.Form):
    TARGETS: list[tuple[str, str]] = [('patient', 'Patient'), ('physio', 'Physiotherapist')]

    emails = forms.CharField(
        max_length=255,
        widget=forms.Textarea,
        strip=True,
        required=True,
        label="Email Addresses",
        help_text="Enter email addresses separated by commas, spaces, or new lines."
    )
    target = forms.ChoiceField(
        choices=TARGETS,
        label="Invite As",
        widget=forms.RadioSelect,
        required=True
    )

    def extract_emails(self):
        collected_emails = self.cleaned_data.get('emails')
        # Use regex to split the emails by commas, spaces, or new lines
        email_list = re.split(r'[,\s]+', collected_emails)
        # Validate and filter out invalid emails
        valid_emails = []
        for email in email_list:
            try:
                validate_email(email)
                valid_emails.append(email)
            except ValidationError as ex:
                # Log invalid email if needed
                logger.error(f"Invalid email: {email} - {ex.message}")
                self.add_error('emails', f"Invalid email: {email}")
        return valid_emails

