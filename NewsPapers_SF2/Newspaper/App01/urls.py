from django.contrib import admin
from django.urls import path
from App01.views import index

urlpatterns = [
    path("index", index),
]