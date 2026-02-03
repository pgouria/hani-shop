
# EVENT SYSTEM

SUBSCRIBTION = {}

def subscribe(event, callback):
    SUBSCRIBTION.setdefault(event, []).append(callback)

def publish(event):
    for callback in SUBSCRIBTION.get(event, []):
        callback()
    

# EVENTS

class OrdersCreated:
    def __init__(self, orders):
        self.orders = orders