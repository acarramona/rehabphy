# teams/models.py

from django.db import models

from accounts.models import User

class PhysioTeam(models.Model):
    #Gender choices
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'physio_teams'
    
    def __str__(self) -> str:
        return (
            f'name:{self.first_name} {self.last_name}, phone:{self.phone}, '
            f'created_at:{self.created_at}, updated_at:{self.updated_at}'
        )

    def get_full_name(self):
        return  f'{self.first_name} {self.last_name}'