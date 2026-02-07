from core.plugins.base import BaseChannelPlugin
from inventory.services import InventoryService
from .domain.services import get_prices
from .models import Variant as DGVariant

class DigikalaPlugin(BaseChannelPlugin):
    plugin_name = "digikala"
    code = "digikala"
    def get_price(self,*, variant ,**kwargs):
        get_prices(variants=[variant])
    def is_available(self,*, variant ,**kwargs):
        InventoryService.reserve(variant=variant, quantity=1)
    def is_published(self,*, variant ,**kwargs):
        DGVariant.objects.filter(linked_variant=variant).first().is_active
    def get_stock(self, *, variant, **kwargs):
        DGVariant.objects.filter(linked_variant=variant).first().selling_stock