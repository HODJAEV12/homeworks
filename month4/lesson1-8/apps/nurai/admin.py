from django.contrib import admin
from .models import Students

@admin.register(Students)
class AminStudents(admin.ModelAdmin):
    list_display = ("id", "name", "age", "city")
    search_fields = ("name", "city")