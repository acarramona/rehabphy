# accounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import User
from teams.models import PhysioTeam
from patients.models import Patient
from physios.models import Physio

@receiver(post_save, sender=User)
def create_user_profile(sender:User, instance:User, created:bool, **kwargs):
    if created:
        if instance.user_type == 'PHYSIO_TEAM':
            PhysioTeam.objects.create(user=instance)
        elif instance.user_type == 'PHYSIO':
            Physio.objects.create(user=instance)
        elif instance.user_type == 'PATIENT':
            Patient.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender:User, instance:User, **kwargs):
    if instance.user_type == 'PHYSIO_TEAM':
        instance.physioteam.save()
    elif instance.user_type == 'PATIENT':
        instance.patient.save()
    elif instance.user_type == 'PHYSIO':
        instance.physio.save()