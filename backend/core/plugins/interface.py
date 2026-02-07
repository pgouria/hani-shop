
from dataclasses import dataclass
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from shop.models import Variant


@dataclass(frozen=True, slots=True)
class OrderItemObject:
    variant: "Variant"
    quantity: int

    def __post_init__(self):
        if self.quantity <= 0:
            raise ValueError("quantity must be a positive integer")
    
 

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

    
