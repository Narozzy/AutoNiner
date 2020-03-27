from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import TaskForm
from .models import Task

# Create your views here.
def index(request):
    all_tasks = Task.objects.all()
    return render(request, 'index.html', context={'tasks': all_tasks})

def CreateTask(request):
    content = {'current_user': request.user}
    if request.method == 'POST':
        print(request.POST)
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    elif request.method == 'GET':
        # This will retrieve the form
        content.update({'form': TaskForm()})
    return render(request, 'create_task.html', context=content)