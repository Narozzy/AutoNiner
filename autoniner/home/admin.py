from django.contrib import admin
from .models import Task, DoorCountInstance, QuestionsInstance

# Register your models here.
admin.site.register(Task)
admin.site.register(DoorCountInstance)
admin.site.register(QuestionsInstance)