from django.shortcuts import render
from django.http import HttpResponse
from .forms import TaskForm

# Create your views here.
def index(request):
    return render(request, 'index.html', context={'hello': 'world'})

def CreateTask(request):
    content = {'current_user': request.user}
    if request.method == 'POST':
        print(request.POST)
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'index.html', {})
    elif request.method == 'GET':
        # This will retrieve the form
        content.update({'form': TaskForm()})
    return render(request, 'create_task.html', context=content)