from datetime import datetime

from django.shortcuts import render
from .models import *
from django.views.generic import ListView, DetailView


class ProductsList(ListView):
    model = Product
    ordering = 'name'
    template_name = 'simpleapp/products.html'
    context_object_name = 'products'
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['sale'] = None
        return context


class ProductDetail(DetailView):
    model = Product
    template_name = 'simpleapp/product.html'
    context_object_name = 'product'

