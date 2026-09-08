from django.contrib import admin

from .models import Cars

@admin.register(Cars)
class AdminBooks(admin.ModelAdmin):
    list_display = (
        "id", "brand", "color", "mileage", "transmission_type", "fuel_type", "car_type",
        "car_description", "state", "year", "price", "image"
    )
    search_fields = ("brand", "author")