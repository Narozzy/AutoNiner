import json
import pdb
import utils.excel_automation as ea
import time
import datetime
from decimal import *
from django.core import serializers
from django.shortcuts import render,redirect,HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from .forms import TaskForm, DoorCountInstanceForm
from .models import Task, DoorCountInstance

task_type_map = {
    'DOOR': DoorCountInstance,

}

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
        df_csv = ea.csv_transform(task_objs, t.task_type)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}_{}.csv'.format(t.task_type, time.strftime('%Y%m%d_%H%M%S'))
        df_csv.to_csv(path_or_buf=response, index=False)
        return response
    return render(request, 'excel_template.html', context={'id': t.task_id, 'task_type': t.task_type})

def VisualizationPage(request,id):
    t = Task.objects.get(task_id=id)
    i = task_type_map[t.task_type].objects.all()
    if i:
        min_range = datetime.datetime.utcfromtimestamp((i.order_by('-start_time').first().start_time - 25569) * Decimal(86400.0))
        max_range = datetime.datetime.utcfromtimestamp((i.order_by('end_time').first().end_time - 25569) * Decimal(86400.0))
    else:
        min_range, max_range = '', ''
    if request.method == 'POST':
        start_date = convert_to_serial(datetime.datetime.strptime(request.POST['start_date'], '%m/%d/%Y'))
        end_date = convert_to_serial(datetime.datetime.strptime(request.POST['end_date'], '%m/%d/%Y'))
        instances = task_type_map[t.task_type].objects.filter(task_id=t).filter(start_time__gte=start_date).filter(end_time__lte=end_date)
        # instances = task_type_map[t.task_type].objects.filter(task_id=t)
        breakpoint()
    return render(request, 'data_visualization.html', context={'id':t.task_id, 'task_type': t.task_type, 'min_range': min_range, 'max_range': max_range})

def delete(request, id):
    t = Task.objects.get(task_id=id)
    if t:
        t.delete()
    return redirect('home')

def details(request, id):
    t = Task.objects.get(task_id=id)
    return render(request, 'data_visualization.html', context={'task':t})


""" Helper Functions """
def convert_to_serial(dt: datetime.datetime):
    temp = datetime.datetime(1899, 12, 30)
    delta = dt - temp
    return Decimal(delta.days) + (Decimal(delta.seconds) / 86400)