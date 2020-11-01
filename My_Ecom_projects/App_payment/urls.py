from django.urls import path
from .views import checkout,payment,complitpay,perches
app_name='App_payment'

urlpatterns=[
    path('checkout/',checkout,name='checkout'),
    path('pay/',payment,name='payment'),
    path('com/',complitpay,name='complite'),
    path('parch/<val_id>/<tran_id>/',perches,name='perches')
]