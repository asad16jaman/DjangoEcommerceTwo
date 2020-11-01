from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView
from .models import Category, Product
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

class Home(ListView):
    model = Product
    template_name = 'App_Shop/home.html'
    context_object_name = 'all_product'


class Detail_product(LoginRequiredMixin, DetailView):
    model = Product
    context_object_name = 'myproduct'
    template_name = 'App_Shop/productdetail.html'


