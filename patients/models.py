# patients/models.py

from django.db import models
from accounts.models import User
from physios.models import Physio
from datetime import timedelta
from django.utils import timezone

class Patient(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    physio = models.ForeignKey(Physio, related_name='patients', on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'patients'
    
    def __str__(self):
        return (
            f'name: {self.first_name} {self.last_name}, gender: {self.gender}, address: {self.address}, '
            f'phone: {self.phone}, created_at: {self.created_at}, updated_at: {self.updated_at}'
        )
    
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'


class PersonalNote(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='personal_notes')  # Link to Patient instead of User
    note = models.TextField()
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Note by {self.patient.get_full_name()} on {self.date_added}"


class Medication(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medications')
    note = models.TextField()  # Medication details
    frequency_per_day = models.PositiveIntegerField()  # Frequency of medication per day
    prescribed_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Medication for {self.patient.get_full_name()} - Prescribed on {self.prescribed_date}"

class TherapySession(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='therapy_sessions')
    session_date = models.DateTimeField()  # Date and time of the therapy session
    notes = models.TextField(default='No notes available')  # Set default value

    def __str__(self):
        return f"Session on {self.session_date} for {self.patient.get_full_name()}"

    class Meta:
        ordering = ['session_date']
