# from django.shortcuts import render, get_object_or_404
# physios/views.py

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from patients.models import Patient
from physios.models import Physio
from django.core.exceptions import PermissionDenied

# Custom permission check for the physio role
def is_physio(user):
    if user.is_authenticated and user.groups.filter(name='PHYSIO').exists():
        return True
    else:
        raise PermissionDenied('Access restricted to Physio.')

@login_required
@user_passes_test(is_physio)
def physio_dashboard(request):
    # Ensure the Physio object is retrieved or return 404
    physio = get_object_or_404(Physio, user_id=request.user.id)
    qualifications = physio.qualifications  
    experience_years = physio.experience_years
    # Retrieve all patients related to this physio (assuming a ForeignKey exists)
    patients = Patient.objects.filter(physio=physio)
    patient_count = patients.count()

    # Retrieve assessments related to the physio
    assessments = physio.assessments.all()

    context = {
        'physio': physio,
        'patients': patients,
        'patient_count': patient_count,
        'assessments': assessments,
        'qualifications': qualifications,
        'experience_years': experience_years,
    }

    return render(request, 'physios/physio_dashboard.html', context)