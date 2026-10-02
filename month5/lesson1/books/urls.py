from django.urls import path
from .views import BooksApi

urlpatterns = [
    path('books/', BooksApi.as_view(), name='books-api')
]