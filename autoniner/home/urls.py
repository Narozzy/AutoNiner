from django.urls import path, include
from . import views

urlpatterns = [
    path('home/', views.index, name='home'),
    path('home/task/new', views.CreateTask, name='newTask'),
    path('delete/<int:id>', views.delete),
]