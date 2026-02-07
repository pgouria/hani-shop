from django.apps import AppConfig


class DigikalaConfig(AppConfig):
    name = 'marketplace.digikala'
    def ready(self):
        from core.domain.events import subscribe 
        from core.domain.inventory import StockChanged
        from .handlers import on_stock_changed

        subscribe(StockChanged, on_stock_changed)
