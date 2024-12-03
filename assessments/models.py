# assessments/models.py

from django.db import models
from patients.models import Patient
from physios.models import Physio



class Assessment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='assessments')
    physio = models.ForeignKey(Physio, on_delete=models.CASCADE, related_name='assessments')
    pain_level = models.IntegerField()
    therapy_compliance = models.TextField()
    soap_notes = models.TextField()
    assessment_date = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'assessments'

    def __str__(self):
        return f"Assessment for {self.user.username} on {self.created_at}"

class ROMMeasurement(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='rom_measurements')
    limb_type = models.CharField(max_length=20)  # e.g., 'Upper Limb' or 'Lower Limb'
    limb = models.CharField(max_length=55)       # e.g., 'Right Shoulder'
    movement = models.CharField(max_length=50)   # e.g., 'Flexion'
    assessed_value = models.DecimalField(max_digits=5, decimal_places=2)
    expected_value = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        db_table = 'rom_measurements'

    def __str__(self):
        return f"{self.limb} {self.movement} ({self.assessed_value}°, expected {self.expected_value}°)"
