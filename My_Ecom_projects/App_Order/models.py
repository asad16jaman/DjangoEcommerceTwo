from django.db import models
from django.conf import settings
from App_Shop.models import Product

# Create your models here.
class Card(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='cart')
    item=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='cart')
    quentity=models.IntegerField(default=1)
    purecesh=models.BooleanField(default=False)
    created=models.DateTimeField(auto_now_add=True)
    update=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.quentity}X{self.item}'

    def get_total(self):
        total=self.item.price * self.quentity
        float_total=format(total,'0.2f')
        return float_total


class Order(models.Model):
    orderitem=models.ManyToManyField(Card)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ordered=models.BooleanField(default=False)
    created=models.DateTimeField(auto_now_add=True)
    paymentId=models.CharField(max_length=264,null=True,blank=True)
    orderId=models.CharField(max_length=264,blank=True,null=True)

    def get_totals(self):
        total=0
        for item in self.orderitem.all():
            total += float(item.get_total())
        return total