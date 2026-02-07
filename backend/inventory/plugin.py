from core.plugins.interface import InventoryInterface
from .models import   Stock
from .services import _get_available_stocks ,_get_allocated_stocks
from django.db import transaction

class WarehousePlugin(InventoryInterface):
    plugin_name = "warehouse"
    code = "warehouse"

    @transaction.atomic
    def reserve(self,*, variant, quantity ):
        reserved = 0
        available_stocks = _get_available_stocks(variant)
        for stock in available_stocks:
            available = stock.get_available()
            allocate_amount = min(available, quantity)
            stock.allocated += allocate_amount
            stock.save()
            reserved += allocate_amount
            if reserved == quantity:
                break
        if reserved != quantity:
            raise Exception("Not enough stocks")
        
    @transaction.atomic
    def release(self,*, variant, quantity ):
        allocated_stocks = _get_allocated_stocks(variant)
        for stock in allocated_stocks:
            allocated = stock.allocated
            release_amount = min(allocated, quantity)
            stock.allocated -= release_amount
            stock.save()
            quantity -= release_amount
            if quantity == 0:
                break
        if quantity != 0:
            raise Exception("Not enough allocated stocks")
        
    @transaction.atomic
    def commit(self,*, variant, quantity):
        allocated_stocks = _get_allocated_stocks(variant)
        for stock in allocated_stocks:
            allocated = stock.allocated
            commit_amount = min(allocated, quantity)
            stock.allocated -= commit_amount
            stock.quantity -= commit_amount
            stock.save()
            quantity -= commit_amount
            if quantity == 0:
                break
        if quantity != 0:
            raise Exception("Not enough allocated stocks")
        
    def get_stock(self, *, variant, **kwargs) -> int:
        stocks = Stock.objects.filter(variant=variant)
        count = 0
        if stocks:
            for stock in stocks:
                count += stock.get_available()
            return count
        else:
            return 0
