from django.urls import path
from .views import *

urlpatterns = [
    path('', ProductsList.as_view()),
    path('<int:pk>', ProductDetail.as_view(), name='product_detail'),
]
