from django.urls import path
from .views import *

urlpatterns = [
    path('', PostList.as_view(), name='posts_list'),
    path('filter/', PostListFilter.as_view(), name='posts_filter'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete_url'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='post_update_url'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('add/', PostAdd.as_view(), name='post_add'),
]