
from typing import List
# item class
class OrderItemObject:
    def __init__(self, *, variant, quantity):
       
        self.variant = variant
        self.quantity = quantity
    
 

class InventoryInterface:
    plugin_name = "base"
    code = "base"
    priority = 100
    def reserve(self,*, variant, quantity ):
        raise NotImplementedError
    def release(self,*, variant, quantity ):
        raise NotImplementedError
    def commit(self,*, variant, quantity):
        raise NotImplementedError
    def get_stock(self,*, variant):
        raise NotImplementedError


class ChannelInterface:
    plugin_name = "base"
    code = "base"
    def get_price(self,*, variant ,**kwargs):
        """
        Return Decimal
        """
        raise NotImplementedError
    def get_stock(self,*, variant ,**kwargs):
        """
        Return Decimal
        """
        raise NotImplementedError
    def is_available(self,*, variant ,**kwargs):
        """
        Return Boolean
        """
        raise NotImplementedError
    def is_published(self,*, variant ,**kwargs):
        """
        Return Boolean
        """ 
        raise NotImplementedError
    def place_order(self,*, items : List[OrderItemObject], user):
        raise NotImplementedError

    