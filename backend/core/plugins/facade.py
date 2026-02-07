from orders.services import place_order as place_order_service


def place_order_channel(self,*, items , user):
        result = place_order_service(items=items, channel=self, user=user)
        return result