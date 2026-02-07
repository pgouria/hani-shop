from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _
from typing import List , Type
from django.conf import settings
from core.plugins.interface import   ChannelInterface ,InventoryInterface
from channels.models import Channel



def get_inventory_plugin() -> List[Type[InventoryInterface]]:
    try:
        plugins = []
        for path in settings.INVENTORY_PLUGIN:
           
            try:
                plugin_cls = import_string(path)
                if issubclass(plugin_cls, InventoryInterface):
                    plugins.append(plugin_cls())
            except Exception as e:
                raise ImproperlyConfigured(_(
                    "Could not import inventory plugin %s. Please make sure it is "
                    "listed in the settings.py file and is a subclass of "
                    "InventoryInterface." % path
                ))
        return plugins
    except Exception as e:
        raise ImproperlyConfigured(_(
            "Could not import inventory plugin %s. Please make sure it is "
            "listed in the settings.py file and is a subclass of "
            "InventoryInterface." % settings.INVENTORY_PLUGIN
        ))
    
def get_channel_plugin() -> List[Type[ChannelInterface]]:
    try:
        plugins = []
        # get channel plugin from settings as a list 
        for path in settings.CHANNEL_PLUGIN:
           
            try:
                plugin_cls = import_string(path)
                if issubclass(plugin_cls, ChannelInterface):
                    plugins.append(plugin_cls())
            except Exception as e:
                raise ImproperlyConfigured(_(
                    "Could not import channel plugin %s. Please make sure it is "
                    "listed in the settings.py file and is a subclass of "
                    "ChannelInterface." % path
                ))
        return plugins
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

        

       self.channel = []
       self.inventory = []

    def load_plugins(self):
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