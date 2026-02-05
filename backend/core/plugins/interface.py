

class PricingInterface:
    plugin_name = "base"
    priority = 100
    def get_price(self,*, product, channel ,**kwargs):
        """
        Return Decimal or None
        None = I don't handle this case
        """
        raise NotImplementedError

class InventoryInterface:
    plugin_name = "base"
    priority = 100
    def reserve(self,*, product, quantity , channel=None):
        raise NotImplementedError
    def release(self,*, product, quantity ):
        raise NotImplementedError
    def commit(self,*, product, quantity):
        raise NotImplementedError