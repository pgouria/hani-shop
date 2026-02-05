from core.plugins.registry import registry


class InventoryService:
    

    @staticmethod
    def reserve(product, quantity, channel=None):
        for plugin in registry.get_inventory():
            handled = plugin.reserve(product, quantity, channel)
            if handled:
                return
        raise Exception("No inventory plugin handled reservation")