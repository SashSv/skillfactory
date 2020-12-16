from django.shortcuts import render
from App01.models import *

# Create your views here.
def index(request):
    car = Cars.objects.all()
    return render(request, "index.html", context = {'car':car})