from core.domain.orders import OrdersCreated
from .plugins.telegram import send_orders_notification



def on_orders_created(event: OrdersCreated):
    
    send_orders_notification(event.orders)
      
        
