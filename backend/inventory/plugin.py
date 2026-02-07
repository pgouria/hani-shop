from core.plugins.interface import InventoryInterface
from .models import Warehouse , WarehouseLocation , Stock
from  django.db.models import F

class WarehousePlugin(InventoryInterface):
    plugin_name = "warehouse"
    code = "warehouse"

    def reserve(self,*, variant, quantity ):
        pass
    def release(self,*, variant, quantity ):

        pass
    def commit(self,*, variant, quantity):
        pass
    def get_stock(self, *, variant, **kwargs):
        stocks = Stock.objects.filter(variant=variant)
        count = 0
        if stocks:
            for stock in stocks:
                count += stock.get_available()
            return count
        else:
            return 0
