from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

class HelloView(APIView):
    def get(self, request):
        return Response({
            "message": "Hello from class!"
        })

@api_view(['GET'])
def hello_view(request):
    return Response({
        "message": "Hello from function!"
    })

class People(APIView):
    def get(self, request):
        return Response({
            "name": "Abdulloh",
            "city": "Osh",
            "year": 2012,
            "geo": "Geeks"
        })

@api_view(['GET'])
def people_func(request):
    return Response({
        "name": "Abdulloh",
        "city": "Osh",
        "year": 2012,
        "geo": "Geeks"
    })