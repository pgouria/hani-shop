import logging  
from core.plugins.registry import registry
from typing import List
from .models import Stock

logger = logging.getLogger(__name__)


class InventoryService:
   

    @staticmethod
    def reserve(variant, quantity):
       
        for plugin in registry.inventory:
            handled = plugin.reserve(variant=variant, quantity=quantity)
            if handled:
                return
        raise Exception("No inventory plugin handled reservation")
    @staticmethod
    def get_stock(variant):
     
       
        for plugin in registry.inventory:
            handled = plugin.get_stock(variant=variant)
           
            
            return handled
    


def _get_available_stocks(variant) -> List[Stock]:
        """get available stocks for a variant"""
        
        available_stocks = []
        for stock in Stock.objects.filter(variant=variant):
            stock.get_available()
            available_stocks.append(stock)
        return available_stocks


def _get_allocated_stocks(variant) -> List[Stock]:
        """get allocated stocks for a variant"""
        
        allocated_stocks = []
        for stock in Stock.objects.filter(variant=variant , allocated__gt=0):
            allocated_stocks.append(stock)
            
        return allocated_stocks