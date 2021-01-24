from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from .models import *
from .filters import PostFilter
from .forms import PostForm
from django.shortcuts import redirect



from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

from django.contrib.sites.shortcuts import get_current_site

# test for celery
from django.http import HttpResponse
from .tasks import hello, printer
from django.views import View

# Create your views here.

class IndexView(View):
    def get(self, request):
        printer.delay(10)
        hello.delay()
        return HttpResponse('Hello!')


@login_required
def category_subscribe(request, cat_id):
    category = Category.objects.get(id=cat_id)
    subscribers_list = User.objects.all().filter(categories=category)

    if request.user not in subscribers_list:
        category.subscribers.add(request.user)

    response = redirect('/news/categories/')
    return response



def post_add_redirect(request):
    response = redirect('/accounts/login/')
    return response


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



class CategoryPostList(ListView):
    model = Category
    template_name = 'blogapp/category_list.html'
    context_object_name = 'category_list'
    ordering = ['name']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = Category.objects.all().filter(subscribers=self.request.user)
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
            categories = Category.objects.filter(posts=new_post)
            subscribers_email_list = []

            for cat in categories:
                cat_subscribers = list(User.objects.filter(categories=cat))
                subscribers_email_list += cat_subscribers

            for user in set(subscribers_email_list):

                html_content = render_to_string(
                    'blogapp/new_post_mail.html',
                    {
                        'new_post': new_post,
                        'user': user,
                        'site_domain': get_current_site(request).domain, # подставляем адрес домена автоматом в письмо
                    }
                )

                msg = EmailMultiAlternatives(
                    subject = f'{new_post.header[:20]} - Sasha blog',
                    body = '',
                    from_email='sendme.email@yandex.ru',
                    to=[user.email, ]
                )

                msg.attach_alternative(html_content, 'text/html')
                msg.send()

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