from core.plugins.base import BaseChannelPlugin
from inventory.services import InventoryService
import logging
logger = logging.getLogger(__name__)

class WebSiteChannelPlugin(BaseChannelPlugin):
    plugin_name = "website"
    code = "website"
    def get_price(self,*, variant ,**kwargs):
        return variant.base_price
    def is_available(self,*, variant ,**kwargs):
        stock = InventoryService.get_stock(variant=variant)
        
        if stock > 0:
                return True
        else:
              
                return False
   
        
    def is_published(self, *, variant, **kwargs):
        return True
    def get_stock(self, *, variant, **kwargs):
        return InventoryService.get_stock(variant=variant)