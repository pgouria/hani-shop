from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from cart.utils.cart import Cart
from .forms import QuantityForm
from shop.models import Variant
import logging
logger = logging.getLogger(__name__)




def add_to_cart(request):
    if request.method != "POST":
        return redirect("/")

    form = QuantityForm(request.POST)
    if not form.is_valid():
        messages.error(request, "اطلاعات ارسال شده نامعتبر است")
        return redirect(request.META.get("HTTP_REFERER"))
    

    variant = request.POST.get("variant")
    quantity = form.cleaned_data["quantity"]
  
    cart = Cart(request)

    variant= Variant.objects.get(id=variant)
    price =request.channel.get_price(variant=variant)
   
    cart.add(variant=variant, quantity=quantity, price=price)

   

    messages.success(request, "به سبد خرید اضافه شد")
    return redirect(request.META.get("HTTP_REFERER"))



@login_required
def show_cart(request):
    cart = Cart(request)
    context = {'title': 'سبد خرید', 'cart': cart}
    return render(request, 'cart.html', context)


@login_required
def remove_from_cart(request, variant_id):
    cart = Cart(request)
    variant = get_object_or_404(Variant, id=variant_id)
    cart.remove(variant)
    return redirect('cart:show_cart')