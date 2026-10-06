from django.contrib import admin
from .models import Car

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('id', 'make', 'model', 'year', 'price')
    search_fields = ('make', 'model')
    list_filter = ('year',)