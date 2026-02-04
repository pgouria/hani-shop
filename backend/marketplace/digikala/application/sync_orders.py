from ..infrastructure.digikala_api import DigikalaClient
from ..domain.services import save_orders
from core.domain.events import publish , OrdersCreated





def sync_orders():

    digikala_client = DigikalaClient()
    orders = digikala_client.fetch_orders()
    new_orders = save_orders(orders)
    if new_orders:
        publish(OrdersCreated(new_orders))

    