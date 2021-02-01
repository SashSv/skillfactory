from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from blogapp.models import Category
from blogapp.views import category_subscribe

# Create your views here.

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/index.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        context['user_subscribed_categories'] = Category.objects.all().filter(subscribers=self.request.user)
        context['categories_list'] = Category.objects.all()

        return context