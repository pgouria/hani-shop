

from core.plugins.registry import registry

class PricingService:

    @staticmethod
    def get_price(variant, channel):
        for plugin in registry.get_pricing():
            price = plugin.get_price(
                variant=variant,
                channel=channel
            )
            if price is not None:
                return price

        raise Exception("No pricing plugin returned a price")
