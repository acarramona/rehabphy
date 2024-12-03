from django import forms
from django.forms import inlineformset_factory
from .models import Assessment, ROMMeasurement


class AssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment  
        fields = ['pain_level', 'therapy_compliance', 'soap_notes']

class AssessmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = ['pain_level', 'therapy_compliance', 'soap_notes']
        widgets = {
            'therapy_compliance': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'soap_notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'pain_level': forms.NumberInput(attrs={
                'type': 'range',
                'min': 0,
                'max': 10,
                'step': 1,
                'class': 'form-range',
                'oninput': "this.nextElementSibling.value = this.value"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adding additional styling or attributes if needed
        self.fields['pain_level'].label = "Pain Level (0-10)"
        self.fields['therapy_compliance'].label = "Therapy Compliance Notes"
        self.fields['soap_notes'].label = "SOAP Notes"


class ROMMeasurementForm(forms.ModelForm):
    class Meta:
        model = ROMMeasurement
        fields = ['limb_type', 'limb', 'movement', 'assessed_value', 'expected_value']
        widgets = {
            'limb_type': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('Upper Limb', 'Upper Limb'),
                ('Lower Limb', 'Lower Limb'),
                ('Spine', 'Spine'),
            ]),
            'limb': forms.TextInput(attrs={'class': 'form-control'}),
            'movement': forms.TextInput(attrs={'class': 'form-control'}),
            'assessed_value': forms.NumberInput(attrs={'class': 'form-control'}),
            'expected_value': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adding more descriptive labels if needed
        self.fields['limb_type'].label = "Limb Type (e.g., Upper Limb, Lower Limb)"
        self.fields['limb'].label = "Limb (e.g., Right Shoulder)"
        self.fields['movement'].label = "Movement (e.g., Flexion)"
        self.fields['assessed_value'].label = "Assessed Value (in degrees)"
        self.fields['expected_value'].label = "Expected Value (in degrees)"


# Creating an inline formset to manage multiple ROM Measurements for a given Assessment
ROMMeasurementFormSet = inlineformset_factory(
    Assessment,
    ROMMeasurement,
    form=ROMMeasurementForm,
    extra=1,  # Specifies how many empty forms should be rendered by default (for new entries)
    can_delete=True  # Allows the user to delete ROMMeasurement entries
)
