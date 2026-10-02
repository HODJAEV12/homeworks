from django.contrib import admin
from .models import Books

@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'title', 'description', 'price', 'year')
    search_fields = ('author', 'title')
    list_filter = ('year',)