from django.urls import path, re_path
from .views import *


urlpatterns = [
    path('', PostList.as_view(), name='posts_list'),
    path('filter/', PostListFilter.as_view(), name='posts_filter'),
    re_path(r'^categories/sub/(?P<cat_id>\d+)/$', category_subscribe, name='cat'),
    path('categories/<int:pk>', CategoryDetail.as_view(), name='category_detail'),
    path('categories/', CategoryPostList.as_view(), name='category_list'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete_url'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='post_update_url'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('add/accounts/login/', post_add_redirect, name='post_add_redirect'),
    path('add/', PostAdd.as_view(), name='post_add'),
]
