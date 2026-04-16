from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from order.models import Order, Cart
from store.models import Product


from coupon.forms import CouponCodeForm
from coupon.models import Coupon
from django.utils import timezone
from django.contrib import messages
# Create your views here.


@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)

    order_item, created = Cart.objects.get_or_create(
        user=request.user,
        item=item,
        purchased=False
    )

    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.orderitems.filter(item=item).exists():
            size = request.POST.get('size')
            color = request.POST.get('color')
            quantity = request.POST.get('quantity')

            if quantity:
                order_item.quantity += int(quantity)
            else:
                order_item.quantity += 1

            order_item.size = size
            order_item.color = color
            order_item.save()

        else:
            order_item.size = request.POST.get('size')
            order_item.color = request.POST.get('color')

            order.orderitems.add(order_item)

        return redirect('store:index')

    else:
        order = Order.objects.create(user=request.user)
        order.orderitems.add(order_item)
        return redirect('store:index')
    
# def cart_view(request):
#     carts = Cart.objects.filter(user=request.user, purchased=False)
#     orders = Order.objects.filter(user=request.user, ordered=False)
#     if carts.exists() and orders.exists():
#         order = orders[0]


def cart_view(request):
    if not request.user.is_authenticated:
        return redirect('account:login')
    
    # carts = Cart.objects.filter(user=request.user, purchased=False)
    carts = Cart.objects.filter(user=request.user, purchased=False, quantity__gt=0)
    orders = Order.objects.filter(user=request.user, ordered=False)

    # ✅ Initialize সব variable আগে
    order = None
    coupon_form = CouponCodeForm()
    coupon_code = None
    total_price_after_discount = None

    # ✅ Safe order fetch
    if orders.exists():
        order = orders.first()

    # ✅ Coupon apply logic
    if request.method == "POST":
        coupon_form = CouponCodeForm(request.POST)

        if coupon_form.is_valid() and order:
            current_time = timezone.now()
            code = coupon_form.cleaned_data.get('code')

            try:
                coupon_obj = Coupon.objects.get(code=code, active=True)

                if coupon_obj.valid_to >= current_time:
                    get_discount = (coupon_obj.discount / 100) * order.get_totals()
                    total_price_after_discount = order.get_totals() - get_discount

                    request.session['discount_total'] = total_price_after_discount
                    request.session['coupon_code'] = code

                    messages.success(request, "Coupon applied successfully!")
                    return redirect('order:cart')

                else:
                    messages.warning(request, "Coupon expired")

            except Coupon.DoesNotExist:
                messages.error(request, "Invalid coupon code")

    # ✅ Get from session safely
    total_price_after_discount = request.session.get('discount_total')
    coupon_code = request.session.get('coupon_code')

    # ✅ Handle empty cart (important)
    if not carts.exists():
        messages.warning(request, "Your cart is empty")

    context = {
        'carts': carts,
        'order': order,
        'coupon_form': coupon_form,
        'coupon_code': coupon_code,
        'total_price_after_discount': total_price_after_discount,
    }

    return render(request, 'store/cart.html', context)


def remove_item_from_cart(request, pk):
    item = get_object_or_404(Product,pk=pk)
    orders = Order.objects.filter(user=request.user,ordered=False)
    if orders.exists():
        order = orders[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.get(item=item, user=request.user, purchased=False)
            # order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
            order.orderitems.remove(order_item)
            order_item.delete()
            return redirect('order:cart')
        else:
            return redirect('order:cart')
    else:
        return redirect('order:cart')


def increase_cart(request,pk):
    item = get_object_or_404(Product,pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
            if order_item.quantity >=1:
                order_item.quantity +=1
                order_item.save()
                return redirect('order:cart')
            else:
                return redirect('order:cart')
        else:
            return redirect('store:index')
    else:
        return redirect('store:index')

def decrease_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.get(item=item, user=request.user, purchased=False)

            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                # ✅ DELETE instead of 0 quantity
                order.orderitems.remove(order_item)
                order_item.delete()

            return redirect('order:cart')

    return redirect('store:index')


