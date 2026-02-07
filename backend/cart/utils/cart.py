from shop.models import Variant


CART_SESSION_ID = 'cart'


class Cart:
    def __init__(self, request):
        self.session = request.session
        self.cart = self.add_cart_session()

    def __iter__(self):
        variant_ids = self.cart.keys()
        variants = Variant.objects.filter(id__in=variant_ids)
        cart = self.cart.copy()
        for variant in variants:
            cart[str(variant.id)]['variant'] = variant
        for item in cart.values():
            item['total_price'] = int(item['price']) * int(item['quantity'])
            yield item

    def add_cart_session(self):
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        return cart

    def add(self, variant, quantity , * , price):
        variant_id = str(variant.id)

        if variant_id not in self.cart:
            self.cart[variant_id] = {'quantity': 0, 'price': str(price)}

        self.cart.get(variant_id)['quantity'] += quantity
        self.save()

    def remove(self, variant):
        variant_id = str(variant.id)
        if variant_id in self.cart:
            del self.cart[variant_id]
            self.save()

    def save(self):
        self.session.modified = True

    def get_total_price(self):
        return sum(int(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[CART_SESSION_ID]
        self.save()