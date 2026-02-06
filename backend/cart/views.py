from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from cart.utils.cart import Cart
from .forms import QuantityForm
from shop.models import Variant


@login_required
def add_to_cart(request, variant_id):
    cart = Cart(request)
    variant = get_object_or_404(Variant, id=variant_id)
    form = QuantityForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        cart.add(product=variant, quantity=data['quantity'])
        messages.success(request, 'Added to your cart!', 'info')
    return redirect('shop:product_detail', slug=variant.product.slug)


@login_required
def show_cart(request):
    cart = Cart(request)
    context = {'title': 'Cart', 'cart': cart}
    return render(request, 'cart.html', context)


@login_required
def remove_from_cart(request, variant_id):
    cart = Cart(request)
    variant = get_object_or_404(Variant, id=variant_id)
    cart.remove(variant)
    return redirect('cart:show_cart')