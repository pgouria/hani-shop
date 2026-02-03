from .services.api_client import DigikalaClient
from .services.save import save_variants,save_orders
from core.domain.events import publish , OrdersCreated





def fetch_orders():

    digikala_client = DigikalaClient()
    orders = digikala_client.fetch_orders()
    new_orders = save_orders(orders)
    publish(OrdersCreated(new_orders))

    