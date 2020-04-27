import json
import pdb
from utils import excel_automation as ea
import time
import datetime
import io
from decimal import *
from django.core import serializers
from django.shortcuts import render,redirect,HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.pyplot as plt
from .forms import TaskForm, DoorCountInstanceForm
from .models import Task, DoorCountInstance, QuestionsInstance


task_type_map = {
    'DOOR': DoorCountInstance,
    'QUESTIONS': QuestionsInstance
}

# Create your views here.
def index(request):
    if not request.user.is_superuser:
        return redirect('/admin')
    all_tasks = Task.objects.all()
    recent_tasks = Task.objects.order_by('last_modified')[:5]
    return render(request, 'index.html', context={'tasks': all_tasks, 'recent_tasks': recent_tasks})

def CreateTask(request):
    if not request.user.is_superuser:
        return redirect('/admin')
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
    if not request.user.is_superuser:
        return redirect('/admin')
    t = Task.objects.get(task_id=id)
    if request.method == 'POST':
        instances = json.loads(request.POST['template'])
        dc_instances = []
        if t.task_type == 'DOOR':
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
        elif t.task_type == 'QUESTIONS':
            for i in instances:
                dc_instances.append(
                    QuestionsInstance(
                        task = t,
                        id = i['id'],
                        internal_notes = i['Internal Notes'] if 'Internal Notes' in i else '',
                        ip_address = i['IP Address'] if 'IP Address' in i else '',
                        entered_by = i['Entered By'],
                        desk_location = i['Desk/Location'],
                        question = i['Question'] if 'Question' in i else '',
                        question_type = i['Question Type'],
                        date = i['Date']
                    )
                )
            QuestionsInstance.objects.bulk_create(dc_instances)
            task_objs = QuestionsInstance.objects.filter(task_id=t).values()
        t.last_modified = datetime.datetime.now()
        t.save()
        breakpoint()
        df_csv = ea.csv_transform(task_objs, t.task_type)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}_{}.csv'.format(t.task_type, time.strftime('%Y%m%d_%H%M%S'))
        df_csv.to_csv(path_or_buf=response, index=False)
        return response
    return render(request, 'excel_template.html', context={'id': t.task_id, 'task_type': t.task_type})

def VisualizationPage(request,id):
    if not request.user.is_superuser:
        return redirect('/admin')
    t = Task.objects.get(task_id=id)
    i = task_type_map[t.task_type].objects.all()
    if i:
        if t.task_type == 'DOOR':
            max_range = datetime.datetime.utcfromtimestamp((i.order_by('-start_time').first().start_time - 25569) * Decimal(86400.0))
            min_range = datetime.datetime.utcfromtimestamp((i.order_by('end_time').first().end_time - 25569) * Decimal(86400.0))
        elif t.task_type == 'QUESTIONS':
            max_range = datetime.datetime.utcfromtimestamp((i.order_by('-date').first().date - 25569) * Decimal(86400.0))
            min_range = datetime.datetime.utcfromtimestamp((i.order_by('date').first().date - 25569) * Decimal(86400.0)) 
    else:
        min_range, max_range = '', ''
    if request.method == 'POST':
        start_date = convert_to_serial(datetime.datetime.strptime(request.POST['start_date'], '%m/%d/%Y'))
        end_date = convert_to_serial(datetime.datetime.strptime(request.POST['end_date'], '%m/%d/%Y'))
        if t.task_type == 'DOOR':
            instances = task_type_map[t.task_type].objects.filter(task_id=t).filter(start_time__gte=start_date).filter(end_time__lte=end_date).values()
        elif t.task_type == 'QUESTIONS':
            instances = task_type_map[t.task_type].objects.filter(task_id=t).filter(date__gte=start_date).filter(date__lte=end_date).values()
            breakpoint()
        plot = ea.construct_visualization(instances, t.task_type)
        FigureCanvasAgg(plot)
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close(plot)
        response = HttpResponse(buf.getvalue(),content_type = 'image/png')
        return response
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