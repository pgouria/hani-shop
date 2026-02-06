from orders.models import Order

class OrdersCreated:
    def __init__(self, orders : list[Order]):
        self.orders = orders
