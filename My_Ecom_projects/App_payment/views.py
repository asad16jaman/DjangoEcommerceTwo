from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect
from .forms import BillingForm
from .models import BillingAddress
from App_Order.models import Order,Card
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

# for payment
from sslcommerz_python.payment import SSLCSession
from decimal import Decimal
import requests
import socket


# Create your views here.
@login_required()
def checkout(request):
    save_address=BillingAddress.objects.get_or_create(user=request.user)[0]
    order_qs=Order.objects.filter(user=request.user,ordered=False)
    order_item=order_qs[0].orderitem.all()
    total_order=order_qs[0].get_totals()

    form=BillingForm(instance=save_address)
    if request.method == 'POST':
        form=BillingForm(request.POST,instance=save_address)
        if form.is_valid():
            form.save()
            messages.success(request,'successfully registered............')

    return render(request,'App_payment/checkout.html',context={'form':form,'order_item':order_item,'total':total_order,'save_address':save_address})


@login_required()
def payment(request):
    saved_address=BillingAddress.objects.get_or_create(user=request.user)[0]
    if not saved_address.is_fully_filled():
        messages.info(request,'inter Shipping address properly')
        return redirect("App_payment:checkout")

    if not request.user.profile.is_fully_filled():
        messages.info(request,'full field to your profile ')
        return redirect('app_login:profile')
    # payment getway is started hare---------------------------------------------------------------------
    stror_id = 'asadu5f9ab871f41b5'  #mail enformation ssl send me in my email
    api_key = 'asadu5f9ab871f41b5@ssl' #mail enformation ssl send me in my email
    mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id=stror_id,
                            sslc_store_pass=api_key)
    # section two and here is kddkkd---------------------------------------
    status_url=request.build_absolute_uri(reverse("App_payment:complite"))
    mypayment.set_urls(success_url=status_url, fail_url=status_url,
                       cancel_url=status_url, ipn_url=status_url)

    #section three is hare it is very impornt for product------------------
    order_qs=Order.objects.get(user=request.user,ordered=False)
    order_item=order_qs.orderitem.all()
    total_order= order_qs.get_totals()
    mypayment.set_product_integration(total_amount=Decimal(total_order), currency='BDT', product_category='oneck',
                                      product_name=order_item, num_of_item=len(order_item), shipping_method='Curiar',
                                      product_profile='None')

    #section four is hare it is very imporent for customer information ---------
    current_user=request.user
    mypayment.set_customer_info(name=current_user.profile.full_name, email=current_user.email, address1=current_user.profile.address_1,
                                address2=current_user.profile.address_1, city=current_user.profile.city, postcode=current_user.profile.zipcode, country=saved_address.country,
                                phone=current_user.profile.phone)

    # section five is hare it is very imporent for customer information ---------
    mypayment.set_shipping_info(shipping_to=current_user.profile.full_name, address=saved_address.address, city=saved_address.city, postcode=saved_address.zipcode,
                                country=saved_address.country)

    response_data = mypayment.init_payment()
    return redirect(response_data['GatewayPageURL'])


@csrf_exempt
def complitpay(request):
    if request.method == 'POST':
        send_data=request.POST
        # print(send_data)
        status=send_data['status']
        if status == 'VALID':
            rsk_title=send_data['risk_title']
            if rsk_title=='Safe':
                val_id = send_data['val_id']
                tran_id = send_data['tran_id']
                messages.success(request,'your transcktion successfully')
                return HttpResponseRedirect(reverse("App_payment:perches",kwargs={'val_id':val_id,'tran_id':tran_id}))
            if rsk_title != 'Safe':
                val_id = send_data['val_id']
                tran_id = send_data['tran_id']
                messages.info(request,'some risk from tranjecktion but dan...')
                return HttpResponseRedirect(
                    reverse("App_payment:perches", kwargs={'val_id': val_id, 'tran_id': tran_id}))

        if status == 'CANCELLED':
            val_id = send_data['val_id']
            tran_id = send_data['tran_id']
            messages.warning(request,'you have cancle your transcktion')
            return HttpResponseRedirect(reverse("App_payment:perches", kwargs={'val_id': val_id, 'tran_id': tran_id}))
        if status == 'FAILED':
            messages.warning(request,'not success transection happend')
            return render(request,'App_payment/complite.html',context={})

@login_required()
def perches(reques,val_id,tran_id):
    order=Order.objects.get(user=reques.user,ordered=False)
    order.ordered=True
    order.orderId=val_id
    order.paymentId=tran_id
    order.save()
    cart2=Card.objects.filter(user=reques.user,purecesh=False)
    for x in cart2:
        x.purecesh=True
        x.save()
    return redirect('app_shop:home')

