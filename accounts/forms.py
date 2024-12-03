# accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import User

GENDER_CHOICES: list[tuple[str, str]] = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]

class PhysioTeamSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    phone = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields: list[str] = ['email', 'password1', 'password2','first_name', 'last_name', 'phone']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already taken.")
        return email

    def save(self, commit=True):
        user:User = super().save(commit=False)
        user.email = user.email.lower()
        user.username = user.email
        user.user_type = 'PHYSIO_TEAM'

        if commit:
            user.save()
            user.physioteam.first_name = self.cleaned_data.get('first_name')
            user.physioteam.last_name = self.cleaned_data.get('last_name')
            user.physioteam.phone = self.cleaned_data.get('phone')
            user.physioteam.save()
        return user

class PhysioSignUpForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    address = forms.CharField(widget=forms.Textarea)
    phone = forms.CharField(max_length=15)
    license_number = forms.CharField(max_length=30)
    specialties = forms.CharField(max_length=255, widget=forms.Textarea)

    class Meta:
        model = User
        fields: list[str] = ['email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already taken.")
        return email
    
    def save(self, commit=True):
        user:User = super().save(commit=False)
        user.user_type = 'PHYSIO'
        user.email = user.email.lower()
        user.username = user.email
        # Generate a random password
        self.generated_password = User.objects.make_random_password(8)
        user.set_password(self.generated_password)

        if commit:
            user.save()
            user.physio.first_name = self.cleaned_data.get('first_name')
            user.physio.last_name = self.cleaned_data.get('last_name')
            user.physio.gender = self.cleaned_data.get('gender')
            user.physio.address = self.cleaned_data.get('address')
            user.physio.phone = self.cleaned_data.get('phone')
            user.physio.license_number = self.cleaned_data.get('license_number')
            user.physio.specialties = self.cleaned_data.get('specialties')
            user.physio.save()
        return user
    
class PatientSignUpForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    address = forms.CharField(widget=forms.Textarea)
    phone = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields: list[str] = ['email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email = email.lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already taken.")
        return email
    
    def save(self, commit=True):
        user:User = super().save(commit=False)
        user.user_type = 'PATIENT'
        user.email = user.email.lower()
        user.username = user.email
        # Generate a random password
        self.generated_password = User.objects.make_random_password(8)
        user.set_password(self.generated_password)
        if commit:
            user.save()
            user.patient.first_name = self.cleaned_data.get('first_name')
            user.patient.last_name = self.cleaned_data.get('last_name')
            user.patient.gender = self.cleaned_data.get('gender')
            user.patient.address = self.cleaned_data.get('address')
            user.patient.phone = self.cleaned_data.get('phone')
            user.patient.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': True}),
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
    )

    error_messages = {
        'invalid_login': _(
            "Invalid username or password."
        ),
        'inactive': _("This account is inactive."),
    }
def clean(self):
    cleaned_data = super().clean()
    password1 = cleaned_data.get("password1")
    password2 = cleaned_data.get("password2")
    if password1 and password2 and password1 != password2:
        raise forms.ValidationError("Passwords do not match")
    return cleaned_data