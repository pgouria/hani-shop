from django.apps import AppConfig



class NotificationConfig(AppConfig):
    name = 'notification'
    
    def ready(self):
        from core.domain.events import subscribe
        from core.domain.orders import OrdersCreated
        from .handlers import on_orders_created
        subscribe(OrdersCreated, on_orders_created)
        
