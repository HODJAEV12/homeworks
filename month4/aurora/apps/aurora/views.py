from django.shortcuts import render
from .models import (
    Settings, 
    Banner, 
    Advantages, 
    About_hotel,
    Rooms,
)

def index(request):
    settings = Settings.objects.first()
    banner = Banner.objects.first()
    advantages = Advantages.objects.all()
    hotel = About_hotel.objects.first()
    rooms = Rooms.objects.all()
    return render(request, "index.html", locals())

def contact(request):
    return render(request, "contact.html", locals())

def rooms(request):
    return render(request, "rooms.html", locals())