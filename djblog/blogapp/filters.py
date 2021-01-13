from django_filters import FilterSet
from django import forms
from .models import Post
import datetime

class PostFilter(FilterSet):


    class Meta:
        model = Post
        fields = [
            'header',
            'article_text',
            'author',
            'category',
            'created_time',
        ]