from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Cars

class CarListApi(ListView):
    model = Cars
    template_name = "car_list.html"
    context_object_name = "cars"

class CarDetailApi(DetailView):
    model = Cars
    template_name = "car_detail.html"
    context_object_name = "car"