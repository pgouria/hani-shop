from .interface import ChannelInterface
from . facade import place_order_channel

class BaseChannelPlugin(ChannelInterface):
    def place_order(self, *, items, user):
        return place_order_channel(self=self, items=items, user=user)