from django.urls import path
from .views import add_to_card,view_cart,remove_from_cart,increase_card,decrese_card,complate_order

app_name='app_order'

urlpatterns=[
    path('add/<pk>/',add_to_card,name='add'),
    path('cart/',view_cart,name='cart'),
    path('remove/<int:pk>/',remove_from_cart,name='remove'),
    path('add_quentity/<pk>',increase_card,name='increase'),
    path('remove_quentity/<pk>/',decrese_card,name='decrise_quentity'),
    path('complite/',complate_order,name='ordered')
]