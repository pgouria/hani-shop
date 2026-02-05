from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _

from django.conf import settings
from backend.core.plugins.interface import PricingInterface
from core.plugins.interface import InventoryInterface


def get_pricing_plugin():
    try:
        return import_string(settings.PRICING_PLUGIN )
    except ImportError as e:
        raise ImproperlyConfigured(_(
            "Could not import pricing plugin %s. Please make sure it is "
            "listed in the settings.py file and is a subclass of "
            "PricingInterface." % settings.PRICING_PLUGIN
        ))

def get_inventory_plugin():
    try:
        return import_string(settings.INVENTORY_PLUGIN)
    except ImportError as e:
        raise ImproperlyConfigured(_(
            "Could not import inventory plugin %s. Please make sure it is "
            "listed in the settings.py file and is a subclass of "
            "InventoryInterface." % settings.INVENTORY_PLUGIN
        ))
    
class PluginRegistry:
    def __init__(self):

        self.pricing = get_pricing_plugin()
        self.pricing.sort(key=lambda x: x.priority)

        self.inventory = get_inventory_plugin()
        self.inventory.sort(key=lambda x: x.priority)
    def register(self, plugin):
        if issubclass(plugin, PricingInterface):
            self.pricing.append(plugin)
            self.pricing.sort(key=lambda x: x.priority)
        elif issubclass(plugin, InventoryInterface):
            self.inventory.append(plugin)
            self.inventory.sort(key=lambda x: x.priority)
        else:
            raise ImproperlyConfigured(_(
                "Plugin %s is not a subclass of PricingInterface or InventoryInterface." % plugin
            ))
    def get_pricing(self):
        return self.pricing
    def get_inventory(self):
        return self.inventory
    

registry = PluginRegistry()