from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Comment)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    fields = ('header', 'article_text','type','author','category', )
    list_display_links = ('author', 'type', )
    list_display = ('short_header', 'author', 'created_time', 'type', )
    list_filter = ('author', 'created_time', 'type', )
    search_fields = ('header__icontains', 'article_text__icontains')

    empty_value_display = '-empty-'
    filter_horizontal = ('category',)
