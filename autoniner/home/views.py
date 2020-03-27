from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'index.html', context={'hello': 'world'})

def CreateTask(request):
    if request.method == 'POST':
        # This will be after they have completed the form
        pass
    elif request.method == 'GET':
        # This will retrieve the form
        pass
    return render(request, 'create_task.html', context={'form': 'task'})