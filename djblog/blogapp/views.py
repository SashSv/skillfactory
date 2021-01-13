from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from .models import *
from .filters import PostFilter
from .forms import PostForm
from django.shortcuts import redirect

from django.contrib.auth.mixins import PermissionRequiredMixin


# Create your views here.

class PostList(ListView):
    model = Post
    template_name = 'blogapp/post_list.html'
    context_object_name = 'post_list'
    ordering = ['-created_time']
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        return context


class PostListFilter(PostList):
    template_name = 'blogapp/post_filter.html'
    paginate_by = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        return context


class PostAdd(PermissionRequiredMixin, PostList):
    model = Post
    template_name = 'blogapp/post_add.html'
    paginate_by = None
    form_class = PostForm
    permission_required = ('blogapp.add_post')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm()
        return context

    def post(self, request, *args, **kwargs):
        post = self.form_class(request.POST)

        if post.is_valid():
            new_post = post.save()
            return redirect(new_post)


class PostDetail(DetailView):
    model = Post
    template_name = 'blogapp/post_detail.html'
    context_object_name = 'post_detail'


class PostUpdate(PermissionRequiredMixin, UpdateView):
    template_name = 'blogapp/post_update.html'
    form_class = PostForm
    permission_required = ('blogapp.change_post')

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

class PostDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'blogapp/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
    permission_required = ('blogapp.delete_post')