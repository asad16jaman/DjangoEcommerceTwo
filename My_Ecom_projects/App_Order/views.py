from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Order,Card
from App_Shop.models import Product
from django.contrib import messages

# Create your views here.

# @login_required
def add_to_card(request,pk):
    item=get_object_or_404(Product,pk=pk)
    order_item=Card.objects.get_or_create(item=item,user=request.user,purecesh=False)

    order_qs=Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        if order.orderitem.filter(item=item).exists():
            order_item[0].quentity += 1
            order_item[0].save()
            messages.info(request,'this item  was updated.....')
            return redirect('app_shop:home')
        else:
            order.orderitem.add(order_item[0])
            messages.success(request,'your item add successfully ....')
            return redirect('app_shop:home')

    else:
        order=Order(user=request.user)
        order.save()
        order.orderitem.add(order_item[0])
        messages.success(request,'order successfully created ')
        return redirect('app_shop:home')



def view_cart(request):
    carts=Card.objects.filter(user=request.user,purecesh=False)
    orders=Order.objects.filter(user=request.user,ordered=False)
    if carts.exists() and orders.exists():
        order=orders[0]
        return render(request,'App_Order/cart.html',context={'carts':carts,'orders':order})
    else:
        return redirect('app_shop:home')
#
@login_required
def remove_from_cart(request,pk):
    item=get_object_or_404(Product,pk=pk)
    order=Order.objects.filter(user=request.user,ordered=False)
    if order.exists():
        order_item=order[0]
        if order_item.orderitem.filter(item=item).exists():
            myorder=Card.objects.filter(user=request.user,item=item,purecesh=False)[0]
            myorder.delete()
            messages.success(request,'successfully delete.............')
            return redirect('app_order:cart')

        else:
            messages.info(request,'your product not in the cart')

            return redirect('app_shop:home')
    else:
        return redirect('app_shop:home')
#
def increase_card(request,pk):
    item=get_object_or_404(Product,pk=pk)
    order_qs=Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        if order.orderitem.filter(item=item).exists():
            item_order=Card.objects.filter(user=request.user,item=item,purecesh=False)[0]
            if item_order.quentity >=1 :
                item_order.quentity += 1
                item_order.save()
                return redirect('app_order:cart')
            else:
                messages.info(request,f'{item_order.item.name} is not in the cart')
                return redirect('app_shop:home')
        else:
            return redirect('app_shop:home')
    else:
        return redirect('app_shop:home')


@login_required
def decrese_card(request,pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitem.filter(item=item).exists():
            item_order = Card.objects.filter(user=request.user, item=item, purecesh=False)[0]
            if item_order.quentity > 1:
                item_order.quentity -= 1
                item_order.save()
                return redirect('app_order:cart')
            else:
                item_order.delete()
                return redirect('app_order:cart')
        else:
            return redirect('app_shop:home')
    else:
        return redirect('app_shop:home')


def complate_order(request):
    try:
        com_order=Order.objects.filter(user=request.user,ordered=True)
        contex={'order':com_order}
    except:
        contex=None
        messages.info(request,'you havent any order ')
    return render(request,'App_Order/order.html',contex)
