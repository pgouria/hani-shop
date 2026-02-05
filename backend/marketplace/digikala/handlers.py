# NOT IMPLEMENTED
from .models import Variant

def on_stock_changed(payload):
    variant = payload["variant"]

    # map variant → Digikala ID
    mapping = Variant.objects.get(
        marketplace__code="digikala",
        variant=variant
    )

    # call Digikala API (async)
