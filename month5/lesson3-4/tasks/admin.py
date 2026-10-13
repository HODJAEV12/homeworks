from django.contrib import admin
from .models import Task

@admin.register(Task)
class AdminTasks(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'description', 'status',
        'priority', 'due_date', 'created_at', 'updated_at'
    )