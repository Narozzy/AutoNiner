from django.urls import path, include
from . import views

urlpatterns = [
    path('home/', views.index, name='home'),
    path('home/task/new', views.CreateTask, name='newTask'),
    path('delete/<int:id>', views.delete),
    path('details/<int:id>', views.details, name='details'),
    path('template/<int:id>', views.CreateExcelTemplate, name='template'),
    path('visualization/<int:id>', views.VisualizationPage, name='viz'),
    path('about/', views.AboutPage, name='about'),
]