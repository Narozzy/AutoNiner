from django.forms import ModelForm
from .models import Task, DoorCountInstance

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title','description','task_type']

class DoorCountInstanceForm(ModelForm):
    class Meta:
        model = DoorCountInstance
        fields = ['task', 'id','sensor_id','start_time', 'end_time', 'in_count', 'out_count', 'sensor_type', 'ip_address', 'device_type', 'serial_number', 'sensor_group', 'tmestamp']