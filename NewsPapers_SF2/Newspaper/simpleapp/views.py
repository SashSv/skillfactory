# from django.shortcuts import render
from django.views.generic import ListView, DetailView  # импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from .models import Product, Category
from django.core.paginator import Paginator

from .filters import ProductFilter
from .forms import ProductForm

class ProductsList(ListView):

    model = Product  # указываем модель, объекты которой мы будем выводить
    template_name = 'simpleapp/products.html'  # указываем имя шаблона, в котором будет лежать html, в котором будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'products'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через html-шаблон

    form_class = ProductForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ProductFilter(self.request.GET, queryset=self.get_queryset())

        context['categories'] = Category.objects.all()
        context['form'] = ProductForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST запроса

        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не накосячил то сохраняем новый товар
            form.save()

        return super().get(request, *args, **kwargs)
    ordering = ['price']
    paginate_by = 2



class ProductDetail(DetailView):
    model = Product
    template_name = 'simpleapp/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = 'Welcome to Sasha shop'
        return context