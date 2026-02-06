from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _
from typing import List , Type
from django.conf import settings
from core.plugins.interface import   ChannelInterface ,InventoryInterface



def get_inventory_plugin() -> List[Type[InventoryInterface]]:
    try:
        return list(settings.INVENTORY_PLUGIN)
    except Exception as e:
        raise ImproperlyConfigured(_(
            "Could not import inventory plugin %s. Please make sure it is "
            "listed in the settings.py file and is a subclass of "
            "InventoryInterface." % settings.INVENTORY_PLUGIN
        ))
    
def get_channel_plugin() -> List[Type[ChannelInterface]]:
    try:
        # get channel plugin from settings as a list 
        return list(settings.CHANNEL_PLUGIN)
    except Exception as e:
        raise ImproperlyConfigured(_(
            "Could not import channel plugin %s. Please make sure it is "
            "listed in the settings.py file and is a subclass of "
            "ChannelInterface." % settings.CHANNEL_PLUGIN
        ))
    
class PluginRegistry:
    channel: List[Type[ChannelInterface]]
    inventory: List[Type[InventoryInterface]]
    def __init__(self):

        

        # all channel work together
        self.channel = get_channel_plugin()

        self.inventory = get_inventory_plugin()
        self.inventory.sort(key=lambda x: x.priority)
    def register(self, plugin):
        
        if issubclass(plugin, InventoryInterface):
            self.inventory.append(plugin)
            self.inventory.sort(key=lambda x: x.priority)
        elif issubclass(plugin, ChannelInterface):
            self.channel.append(plugin)
        else:
            raise ImproperlyConfigured(_(
                "Plugin %s is not of known types." % plugin
            ))
 
   
    

registry = PluginRegistry()