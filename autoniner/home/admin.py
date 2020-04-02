from django.contrib import admin
from .models import Task, DoorCountInstance

# Register your models here.
admin.site.register(Task)
admin.site.register(DoorCountInstance)