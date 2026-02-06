
class InventoryInterface:
    plugin_name = "base"
    priority = 100
    def reserve(self,*, variant, quantity , channel=None):
        raise NotImplementedError
    def release(self,*, variant, quantity ):
        raise NotImplementedError
    def commit(self,*, variant, quantity):
        raise NotImplementedError


class ChannelInterface:
    plugin_name = "base"
    code = "base"
    def __init__(self, plugin_name, code):
        self.plugin_name = plugin_name
        self.code = code
        if not (self.plugin_name  and self.code):
            raise ValueError("plugin_name, priority and code are required")
    def get_price(self,*, variant, channel ,**kwargs):
        """
        Return Decimal
        """
        raise NotImplementedError
    
    
 