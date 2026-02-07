from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from shop.models import Product, Category
from cart.forms import QuantityForm
import logging 

logger = logging.getLogger(__name__)



def paginat(request, list_objects):
    p = Paginator(list_objects, 20)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except Exception as e:
        raise e
    return page_obj


class ProductCard:
        def __init__(self, product, price):
                self.product = product
                self.price = price

def home_page(request):
    channel = request.channel
    item = []


    products = Product.objects.prefetch_related("variants").all()


    

    for product in products:
        for variant in product.variants.all():
            logger.info('checking variant availability')
            logger.info(channel.is_available(variant=variant))
            if channel.is_available(variant=variant):
                item.append({
                    "product": product,
                    "price": channel.get_price(variant=variant, channel=channel)
                })
                break  # one variant per product for homepage
        
    product_cards = []
    if item:
     for item in item:
      product_cards.append(ProductCard(item["product"], item["price"]))
   
    

    context = {"products": paginat(request, product_cards)}
    return render(request, "home_page.html", context)

class VariantCard:
    def __init__(self, variant, price):
        self.variant = variant
        self.price = price

def product_detail(request, slug):
    channel = request.channel
    form = QuantityForm()
    product = Product.objects.get(slug=slug).prefetch_related("variants")
    variants = product.variants.all()
    to_show_variants = []
    for variant in variants:
        if channel.is_available(variant=variant, channel=request.channel):
            price = channel.get_price(variant=variant, channel=request.channel)
            to_show_variants.append(VariantCard(variant, price))
    related_products = Product.objects.filter(category=product.category).all()[:5]
    context = {
        'title':product.title,
        'product':product,
        'variants':to_show_variants,
        'form':form,
        'favorites':'favorites',
        'related_products':related_products
    }
    if request.user.likes.filter(id=product.id).first():
        context['favorites'] = 'remove'
    return render(request, 'product_detail.html', context)


@login_required
def add_to_favorites(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    request.user.likes.add(product)
    return redirect('shop:product_detail', slug=product.slug)


@login_required
def remove_from_favorites(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    request.user.likes.remove(product)
    return redirect('shop:favorites')


@login_required
def favorites(request):
    products = request.user.likes.all()
    context = {'title':'Favorites', 'products':products}
    return render(request, 'favorites.html', context)


def search(request):
    query = request.GET.get('q')
    products = Product.objects.filter(title__icontains=query).all()
    context = {'products': paginat(request ,products)}
    return render(request, 'home_page.html', context)


def filter_by_category(request, slug):
    """when user clicks on parent category
    we want to show all products in its sub-categories too
    """
    result = []
    category = Category.objects.filter(slug=slug).first()
    [result.append(product) \
        for product in Product.objects.filter(category=category.id).all()]
    # check if category is parent then get all sub-categories
    if not category.is_sub:
        sub_categories = category.sub_categories.all()
        # get all sub-categories products 
        for category in sub_categories:
            [result.append(product) \
                for product in Product.objects.filter(category=category).all()]
    context = {'products': paginat(request ,result)}
    return render(request, 'home_page.html', context)
