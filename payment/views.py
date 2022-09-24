from django.http.response import HttpResponse
from django.urls import reverse
from django.shortcuts import render,redirect
from django.http import HttpResponse

#models
from payment.models import BillingAddress
from payment.forms import BillingAddressForm,PaymentMethodForm
from order.models import Cart, Order

#view
from django.views.generic import TemplateView

class CheckoutTemplateView(TemplateView):
    def get(self, request, *args, **kwargs):
        saved_address = BillingAddress.objects.get_or_create(user=request.user or None)
        saved_address = saved_address[0]
        form = BillingAddressForm(instance=saved_address)
        payment_method = PaymentMethodForm()

        order_qs = Order.objects.filter(user=request.user,ordered=False)
        order_item = order_qs[0].orderitems.all()
        order_total = order_qs[0].get_totals()
    
        context = {
            'billing_address' : form,
            'order_item' : order_item,
            'order_total' : order_total,
            'payment_method' : payment_method,
         
        }
        return render(request, 'store/checkout.html', context)

    def post(self, request, *args, **kwargs):
        saved_address = BillingAddress.objects.get_or_create(user=request.user or None)
        saved_address = saved_address[0]
        form = BillingAddressForm(instance=saved_address)
        payment_obj = Order.objects.filter(user = request.user, ordered=False)[0]
        payment_form = PaymentMethodForm(instance=payment_obj)
        if request.method == 'post' or request.method == 'POST':
            form = BillingAddressForm(request.POST, instance=saved_address)
            pay_form = PaymentMethodForm(request.POST, instance=payment_obj)
            if form.is_valid() and pay_form.is_valid():
                form.save()
                pay_method = pay_form.save()
           
                return redirect('order:cart')
                
                # if not saved_address.is_fully_filled():
                #     return redirect('checkout')



                ### Cash On Delivery Process
                