from django.urls import path
from .views import TaskView, TaskListView, TaskDetailView

urlpatterns = [
    path('tasks/', TaskView.as_view()),
    path('tasks_generics/', TaskListView.as_view()),
    path('tasks_generics/<int:pk>/', TaskDetailView.as_view()),
]