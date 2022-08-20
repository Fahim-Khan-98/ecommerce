from urllib import request
from django.shortcuts import render, get_object_or_404, redirect
from order.models import Order, Cart
from store.models import Product

# Create your views here.


def add_to_cart(request,pk):
    item = get_object_or_404(Product, pk=pk)
    order_item = Cart.objects.get_or_create(user = request.user, item = item, purchased=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            size = request.POST.get('size')
            color = request.POST.get('color')
            quantity = request.POST.get('quantity')
            if quantity:
                order_item[0].quantity += int(quantity)
            else:
                order_item[0].quantity +=1
            order_item[0].size = size
            order_item[0].color = color
            order_item[0].save()
            return redirect('store:index')
        else:
            size = request.POST.get('size')
            color = request.POST.get('color')
            order_item[0].size = size
            order_item[0].color = color

            order.orderitems.add(order_item[0])
            return redirect('store:index')
    else:
        order = Order(user=request.user)
        order.save()
        order.orderitems.add(order_item[0])
        return redirect('store:index')


def cart_view(request):
    carts = Cart.objects.filter(user=request.user, purchased=False)
    orders = Order.objects.filter(user=request.user, ordered=False)
    if carts.exists() and orders.exists():
        order = orders[0]

    context = {
        'order' : order,
        'carts' :carts
    }
    return render (request,'store/cart.html', context)

def remove_item_from_cart(request, pk):
    item = get_object_or_404(Product,pk=pk)
    orders = Order.objects.filter(user=request.user,ordered=False)
    if orders.exists():
        order = orders[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
            order.orderitems.remove(order_item)
            order_item.delete()
            return redirect('order:cart')
        else:
            return redirect('order:cart')
    else:
        return redirect('order:cart')


