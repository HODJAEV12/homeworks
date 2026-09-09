from django.shortcuts import render
from apps.nurai.models import Students

def index(request):
    students = Students.objects.all()
    return render(request, "index.html", locals())