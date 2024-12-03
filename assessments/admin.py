from django.contrib import admin

from assessments.models import Assessment, ROMMeasurement

# Register your models here.
admin.site.register(Assessment)
admin.site.register(ROMMeasurement)