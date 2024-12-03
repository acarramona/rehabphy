from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.text import slugify
from django.utils import timezone
from patients.models import Patient, TherapySession, PersonalNote, Medication
from assessments.models import Assessment
from assessments.forms import AssessmentSubmissionForm, ROMMeasurementFormSet
from .forms import PersonalNoteForm, TherapySessionForm, MedicationForm

# Custom permission check for the patient role
def is_patient(user):
    if user.groups.filter(name='PATIENT').exists():
        return True
    else:
        raise PermissionDenied('Access restricted to patients.')

# Patient dashboard view
@login_required
@user_passes_test(is_patient)
def patient_dashboard(request):
    # Get the patient instance associated with the current user
    patient = get_object_or_404(Patient, user_id=request.user.id)

    # Handle Personal Note Form submission
    if request.method == 'POST' and 'add_note' in request.POST:
        personal_note_form = PersonalNoteForm(request.POST)
        if personal_note_form.is_valid():
            note = personal_note_form.save(commit=False)
            note.patient = patient
            note.save()
            return redirect('patients:patient_dashboard')
    else:
        personal_note_form = PersonalNoteForm()

    # Handle Medication Form submission
    if request.method == 'POST' and 'add_medication' in request.POST:
        medication_form = MedicationForm(request.POST)
        if medication_form.is_valid():
            medication = medication_form.save(commit=False)
            medication.patient = patient
            medication.save()
            return redirect('patients:patient_dashboard')
    else:
        medication_form = MedicationForm()

    # Handle Therapy Session Scheduling Form submission
    if request.method == 'POST' and 'schedule_session' in request.POST:
        session_form = TherapySessionForm(request.POST)
        if session_form.is_valid():
            session = session_form.save(commit=False)
            session.patient = patient
            session.save()
            return redirect('patients:patient_dashboard')
    else:
        session_form = TherapySessionForm()

    # Fetch the patient's scheduled therapy sessions (past and upcoming)
    current_time = timezone.now()
    past_sessions = TherapySession.objects.filter(patient=patient, session_date__lt=current_time)
    upcoming_sessions = TherapySession.objects.filter(patient=patient, session_date__gte=current_time)

    # Fetch assessments, related ROM measurements, personal notes, and medications
    assessments = Assessment.objects.filter(patient=patient).select_related('physio').prefetch_related('rom_measurements').order_by('assessment_date')
    personal_notes = PersonalNote.objects.filter(patient=patient)
    medications = Medication.objects.filter(patient=patient)

    # Determine the assessment period based on the first and last assessment dates
    if assessments.exists():
        start_date = assessments.first().assessment_date.strftime('%d/%m/%Y')
        end_date = assessments.last().assessment_date.strftime('%d/%m/%Y')
        period = f'{start_date} - {end_date}'
    else:
        period = 'No assessments available'

    # Collect ROM data and pain data from assessments
    physios = set()
    rom_data = []
    pain_data = {
        'dates': [],
        'pain_levels': []
    }

    for assessment in assessments:
        date_str = assessment.assessment_date.strftime('%Y-%m-%d')
        pain_data['dates'].append(date_str)
        pain_data['pain_levels'].append(assessment.pain_level)

        physios.add(assessment.physio)

        for measurement in assessment.rom_measurements.all():
            key = f"{measurement.limb} - {measurement.movement}"
            existing_entry = next((entry for entry in rom_data if entry['joint'] == key), None)

            if existing_entry:
                existing_entry['dates'].append(date_str)
                existing_entry['assessed_values'].append(float(measurement.assessed_value))
                existing_entry['expected_values'].append(float(measurement.expected_value))
            else:
                rom_data.append({
                    'joint': key,
                    'slug_key': slugify(key),
                    'dates': [date_str],
                    'assessed_values': [float(measurement.assessed_value)],
                    'expected_values': [float(measurement.expected_value)]
                })

    # Pass context to the template
    context = {
        'patient': patient,
        'physios': physios,
        'assessments': assessments,
        'period': period,
        'pain_data': pain_data,
        'rom_data': rom_data,
        'personal_note_form': personal_note_form,
        'personal_notes': personal_notes,
        'session_form': session_form,
        'past_sessions': past_sessions,
        'upcoming_sessions': upcoming_sessions,
        'medication_form': medication_form,
        'medications': medications,
    }

    return render(request, 'patients/patient_dashboard.html', context)

# Create Assessment View (For Patients)
@login_required
@user_passes_test(is_patient)
def create_assessment(request, patient_id):
    # Get the patient instance associated with the current user
    patient = get_object_or_404(Patient, user_id=patient_id)

    if request.method == 'POST':
        # Initialize the forms with the POST data
        assessment_form = AssessmentSubmissionForm(request.POST)
        rom_measurement_formset = ROMMeasurementFormSet(request.POST)

        if assessment_form.is_valid() and rom_measurement_formset.is_valid():
            # Create and save the assessment instance
            assessment = assessment_form.save(commit=False)
            assessment.patient = patient
            assessment.physio = request.user.physio  
            assessment.save()

            # Associate and save the ROM measurement formset
            rom_measurement_formset.instance = assessment
            rom_measurement_formset.save()

            return redirect('patients:patient_dashboard')
    else:
        # If GET request, initialize empty forms
        assessment_form = AssessmentSubmissionForm()
        rom_measurement_formset = ROMMeasurementFormSet()

    # Pass context to the template
    context = {
        'assessment_form': assessment_form,
        'rom_measurement_formset': rom_measurement_formset,
        'patient': patient,
    }

    return render(request, 'assessments/create_assessment.html', context)

# Schedule Therapy Session View
@login_required
@user_passes_test(is_patient)
def schedule_therapy_session(request):
    patient = get_object_or_404(Patient, user_id=request.user.id)

    if request.method == 'POST':
        form = TherapySessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.patient = patient  # Associate the session with the current patient
            session.save()
            return redirect('patients:patient_dashboard')  # Redirect to the same page after scheduling
    else:
        form = TherapySessionForm()

    # Fetch past and upcoming therapy sessions for the patient
    current_time = timezone.now()
    past_sessions = TherapySession.objects.filter(patient=patient, session_date__lt=current_time)
    upcoming_sessions = TherapySession.objects.filter(patient=patient, session_date__gte=current_time)

    # Pass context to the template
    context = {
        'form': form,
        'past_sessions': past_sessions,
        'upcoming_sessions': upcoming_sessions,
    }

    return render(request, 'patients/schedule_therapy_session.html', context)

# Patient Assessments View
@login_required
@user_passes_test(is_patient)
def patient_assessments(request):
    # Get the patient instance associated with the current user
    patient = get_object_or_404(Patient, user_id=request.user.id)

    # Fetch all assessments related to the patient
    assessments = Assessment.objects.filter(patient=patient).select_related('physio').prefetch_related('rom_measurements').order_by('assessment_date')

    
    context = {
        'patient': patient,
        'assessments': assessments,
    }

    return render(request, 'patients/patient_assessments.html', context)
