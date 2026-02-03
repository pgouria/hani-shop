from django.apps import AppConfig
from core.domain.events import OrdersCreated
from .handlers import send_to_telegram


class NotificationConfig(AppConfig):
    name = 'notification'
    
    def ready(self):
        from core.domain.events import subscribe
        subscribe(OrdersCreated,send_to_telegram)
        
