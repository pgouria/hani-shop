from core.plugins.registry import registry


class InventoryService:
    

    @staticmethod
    def reserve(variant, quantity, channel=None):
        for plugin in registry.inventory:
            handled = plugin.reserve(variant=variant, quantity=quantity, channel=channel)
            if handled:
                return
        raise Exception("No inventory plugin handled reservation")