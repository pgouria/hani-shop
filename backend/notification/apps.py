from django.apps import AppConfig
from core.domain.events import OrdersCreated
from .handlers import on_orders_created


class NotificationConfig(AppConfig):
    name = 'notification'
    
    def ready(self):
        from core.domain.events import subscribe
        subscribe(OrdersCreated, on_orders_created)
        
