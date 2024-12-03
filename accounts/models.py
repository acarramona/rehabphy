# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('patient', 'PATIENT'),
        ('physio', 'PHYSIO'),
        ('physio_team', 'PHYSIO_TEAM'),
    )

   
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)

    # Created at timestamps
    updated_at = models.DateTimeField(auto_now=True)

    # Remove first_name and last_name from the User model
    first_name = None
    last_name = None

    class Meta:
        db_table = 'user_accounts'

    def __str__(self) -> str:
        user_info = f'username: {self.username}, email: {self.email}, is_active: {self.is_active}'
        out_str = ""
        if self.is_superuser:
            out_str = f'{user_info}, is_admin: {self.is_superuser}'
        else:
            out_str = f'{user_info}, is_staff: {self.is_staff}'
        out_str = f'{out_str}, created_at: {self.date_joined}, updated_at: {self.updated_at}'
        return out_str  
