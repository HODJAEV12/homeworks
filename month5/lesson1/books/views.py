from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Books
from .serializer import BooksSerializer

class BooksApi(APIView):
    def get(self, request):
        books = Books.objects.all()
        serializer = BooksSerializer(books, many=True) # many=True указывает, что мы сериализуем список объектов
        return Response(serializer.data, status=status.HTTP_200_OK)