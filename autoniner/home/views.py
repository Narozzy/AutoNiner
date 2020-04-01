from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import TaskForm
from .models import Task

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
    return render(request, 'excel_template.html', context={})

def delete(request, id):
    t = Task.objects.get(task_id=id)
    if t:
        t.delete()
    return redirect('home')

def details(request, id):
    t = Task.objects.get(task_id=id)
    return render(request, 'data_visualization.html', context={'task':t})