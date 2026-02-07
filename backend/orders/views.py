from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib import messages
from core.plugins.interface import OrderItemObject
from orders.models import Order, OrderItem
from cart.utils.cart import Cart


@login_required
def create_order(request):
    if not request.user.address:
        messages.error(request, 'لطفا آدرس خود را وارد کنید', 'danger')
        return redirect('accounts:edit_profile')
    cart = Cart(request)
    items = [item for item in cart]
    items = [OrderItemObject(variant=item['variant'], quantity=item['quantity']) for item in items]
    result = request.channel.place_order(items=items , user=request.user)
    if result.success:
        return redirect('orders:pay_order', order_id=result.order.id)
    else:
        messages.error(request, result.error, 'danger')
        return redirect('orders:user_orders')


@login_required
def checkout(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = {'title':'Checkout' ,'order':order}
    return render(request, 'checkout.html', context)


@login_required
def fake_payment(request, order_id):
    cart = Cart(request)
    cart.clear()
    order = get_object_or_404(Order, id=order_id)
    order.status = True
    order.save()
    return redirect('orders:user_orders')


@login_required
def user_orders(request):
    orders = request.user.orders.all()
    context = {'title':'Orders', 'orders': orders}
    return render(request, 'user_orders.html', context)