# patients/forms.py

from django import forms
from .models import PersonalNote
from .models import TherapySession
from .models import Medication



class PersonalNoteForm(forms.ModelForm):
    class Meta:
        model = PersonalNote
        fields = ['note']  
        widgets = {
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter your personal note here...'}),
        }

class TherapySessionForm(forms.ModelForm):
    class Meta:
        model = TherapySession
        fields = ['session_date', 'notes']

        widgets = {
            'session_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
class MedicationForm(forms.ModelForm):
    class Meta:
        model = Medication
        fields = ['note', 'frequency_per_day']
        widgets = {
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter your medication here...'}),
            'frequency_per_day': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Frequency per day'}),
        }