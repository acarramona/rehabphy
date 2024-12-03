# assessment/views.py

from datetime import datetime
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from patients.models import Patient
from physios.models import Physio
from .forms import AssessmentSubmissionForm, ROMMeasurementFormSet
from assessments.forms import AssessmentForm

@login_required
def create_assessment(request, patient_id):
    patient: Patient = get_object_or_404(Patient, user_id=patient_id)
    if request.method == 'POST':

        assessment_form = AssessmentSubmissionForm(request.POST)
        formset = ROMMeasurementFormSet(request.POST)

        if assessment_form.is_valid() and formset.is_valid():
            assessment = assessment_form.save(commit=False)
            # physio is the logged-in user with a related Physio profile
            assessment.physio = request.user.physio
            assessment.patient = patient
            assessment.save()
            formset.instance = assessment  # Associate the formset with the assessment
            formset.save()
            messages.success(request, "Assessment recorded.")
            return redirect('physios:dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
            print(assessment_form.errors)
            print(formset.errors)
    else:
        assessment_form = AssessmentSubmissionForm()
        formset = ROMMeasurementFormSet()

    return render(request, 'assessments/create_assessment.html', {
        'assessment_form': assessment_form,
        'formset': formset,
        'patient': patient,
        'physio': request.user.physio,
        'assessment_date': datetime.now().strftime('%Y/%m/%d'),
    })

@login_required
def physio_assessments(request, physio_id):
    """
    View to fetch and display all assessments recorded by a specific physio.
    """
    physio: Physio = get_object_or_404(Physio, user_id=physio_id)
    assessments = physio.assessments.select_related('patient').order_by('assessment_date').all()

    context = {
        'physio': physio,
        'assessments': assessments,
    }

    return render(request, 'assessments/physio_assessments.html', context)

@login_required
def fetch_all_patient_assessments(request, patient_id):
    # Get the patient object or return 404 if not found
    patient: Patient = get_object_or_404(Patient, user_id=patient_id)
    
    # Fetch assessments related to the patient
    assessments = (
        patient.assessments
        .select_related('physio')
        .prefetch_related('rom_measurements')
        .order_by('assessment_date')
    )

    # Attempt to get the physio associated with the current user
    try:
        physio = Physio.objects.get(user_id=request.user.id)
    except Physio.DoesNotExist:
        # If not found, use the physio from the first assessment as a fallback
        physio = assessments.first().physio if assessments.exists() else None
    

    # Determine the period based on the first and last assessment dates
    if assessments.exists():
        start_date = assessments.first().assessment_date.strftime('%d/%m/%Y')
        end_date = assessments.last().assessment_date.strftime('%d/%m/%Y')
        period = f'{start_date} - {end_date}'
    else:
        period = 'No assessments available'

    # Initialize data structures
    rom_data = {}
    pain_data = {
        'dates': [],
        'pain_levels': []
    }

    # Collect data from assessments
    for assessment in assessments:
        date_str = assessment.assessment_date.strftime('%Y-%m-%d')
        pain_data['dates'].append(date_str)
        pain_data['pain_levels'].append(assessment.pain_level)

        for measurement in assessment.rom_measurements.all():
            key = f"{measurement.limb} - {measurement.movement}"
            if key not in rom_data:
                # Compute slug_key once per unique key
                slug_key = slugify(key)
                rom_data[key] = {
                    'slug_key': slug_key,
                    'dates': [],
                    'assessed_values': [],
                    'expected_values': []
                }
            rom_data[key]['dates'].append(date_str)
            rom_data[key]['assessed_values'].append(float(measurement.assessed_value))
            rom_data[key]['expected_values'].append(float(measurement.expected_value))
    context = {
        'patient': patient,
        'physio': physio,
        'assessments': assessments,
        'period': period,
        'pain_data': pain_data,
        'rom_data': rom_data,
    }
    return render(request, 'assessments/assessment_detail.html', context)

@login_required
def assessment_success(request):
    """
    View for assessment success page.
    """
    return render(request, 'assessments/assessment_success.html')

@login_required
def fetch_patient_assessment(request, patient_id, assessment_id):
    pass

def fetch_assessment(request,assessment_id):
    pass

@login_required
def fetch_all_assessments(request):
    pass

