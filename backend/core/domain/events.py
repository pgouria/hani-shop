
# EVENT SYSTEM

SUBSCRIBTION = {}

def subscribe(event, callback):
    SUBSCRIBTION.setdefault(event, []).append(callback)

def publish(event):
    for callback in SUBSCRIBTION.get(event, []):
        callback()
    


