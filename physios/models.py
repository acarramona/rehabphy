from django.db import models
from accounts.models import User

class Physio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    qualifications = models.TextField()
    experience_years = models.IntegerField(default=0)  # Added field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.qualifications})'

    class Meta:
        db_table = 'physios'