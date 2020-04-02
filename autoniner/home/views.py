import json
import pdb
import utils.excel_automation as ea
from django.core import serializers
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import TaskForm, DoorCountInstanceForm
from .models import Task, DoorCountInstance

# Create your views here.
def index(request):
    all_tasks = Task.objects.all()
    recent_tasks = Task.objects.order_by('last_modified')[:5]
    return render(request, 'index.html', context={'tasks': all_tasks, 'recent_tasks': recent_tasks})

def CreateTask(request):
    content = {'current_user': request.user}
    if request.method == 'POST':
        print(request.POST)
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            t = Task.objects.all().latest()
            return redirect('template', id=t.task_id)
    elif request.method == 'GET':
        # This will retrieve the form
        content.update({'form': TaskForm()})
    return render(request, 'create_task.html', context=content)

def CreateExcelTemplate(request, id):
    t = Task.objects.get(task_id=id)
    if request.method == 'POST':
        instances = json.loads(request.POST['template'])
        dc_instances = []
        for i in instances:
            dc_instances.append(
                DoorCountInstance(
                    task = t,
                    id = i['id'],
                    sensor_id = i['sensor_id'],
                    start_time = i['start_time'],
                    end_time = i['end_time'],
                    in_count = i['in_count'],
                    out_count = i['out_count'],
                    sensor_type = i['sensor_type'],
                    ip_address = i['ip_address'],
                    device_type = i['device_type'],
                    serial_number = i['serial_number'],
                    sensor_group = i['sensor_group'],
                    tmestamp = i['tmestamp'],
                )
            )
        DoorCountInstance.objects.bulk_create(dc_instances)
        task_objs = DoorCountInstance.objects.filter(task_id=t).values()
        ea.csv_transform(task_objs, t.task_type)
        return redirect('home')
    return render(request, 'excel_template.html', context={'id': t.task_id, 'task_type': t.task_type})

def delete(request, id):
    t = Task.objects.get(task_id=id)
    if t:
        t.delete()
    return redirect('home')

def details(request, id):
    t = Task.objects.get(task_id=id)
    return render(request, 'data_visualization.html', context={'task':t})