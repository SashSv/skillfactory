from django.shortcuts import render
from webinar.models import Good

# Create your views here.
def index(request):
    goods = Good.object.all()
    return render(request, 'index.html', context={'goods': goods, 'name': 'kia rio 3'})