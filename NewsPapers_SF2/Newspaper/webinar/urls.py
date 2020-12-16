from django.contrib import admin
from django.urls import path
from webinar.views import index

urlpatterns = [
    path("index", index),
]