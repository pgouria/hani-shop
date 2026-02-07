import logging  
from core.plugins.registry import registry

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