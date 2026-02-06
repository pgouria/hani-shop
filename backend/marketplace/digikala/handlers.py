# NOT IMPLEMENTED
from .models import Variant as DGVariant
from inventory.models import Stock


def on_stock_changed(stock: Stock):
    # map variant → Digikala ID
    variant = DGVariant.objects.get(linked_variant=stock.variant)


    

    # call Digikala API (async)

    

