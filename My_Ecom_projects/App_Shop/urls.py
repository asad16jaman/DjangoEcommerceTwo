from django.urls import path
from .views import Home,Detail_product


app_name='app_shop'

urlpatterns=[
    path('',Home.as_view(),name='home'),
    path('product/<pk>',Detail_product.as_view(),name='product'),
]