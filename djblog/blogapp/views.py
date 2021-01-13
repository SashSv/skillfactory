from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from .models import *
from .filters import PostFilter
from .forms import PostForm
from django.shortcuts import redirect

# Create your views here.

class PostList(ListView):
    model = Post
    template_name = 'blogapp/post_list.html'
    context_object_name = 'post_list'
    ordering = ['-created_time']
    paginate_by = 3


class PostListFilter(PostList):
    template_name = 'blogapp/post_filter.html'
    paginate_by = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PostAdd(PostList):
    model = Post
    template_name = 'blogapp/post_add.html'
    paginate_by = None
    form_class = PostForm

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


class PostUpdate(UpdateView):
    template_name = 'blogapp/post_update.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

class PostDeleteView(DeleteView):
    template_name = 'blogapp/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'