from django.contrib import admin
from .models import Products

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'price', 'quantity', 'is_available', 'created_at')
    list_filter = ('is_available', 'created_at')
    search_fields = ('title', 'description')