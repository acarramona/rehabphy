# patients/tasks.py

from celery import shared_task
from .models import TherapySession
from django.utils import timezone
from datetime import timedelta

@shared_task
def send_therapy_session_reminder():
    sessions = TherapySession.objects.filter(
        session_date__lte=timezone.now() + timedelta(hours=24),
        reminder_sent=False
    )

    for session in sessions:
        session.send_reminder()
