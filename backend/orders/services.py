from django.db import transaction
from .models import Order, OrderItem
from inventory.services import InventoryService
from core.domain.events import publish
from core.plugins.interface import ChannelInterface
from core.domain.orders import OrdersCreated
from core.plugins.interface import OrderItemObject
from typing import List
import logging
from channels.models import Channel

logger = logging.getLogger('app')

class OrderResult:
    def __init__(self, success, order=None, error=None):
        self.success = success
        self.order = order
        self.error = error


@transaction.atomic
def place_order(*, channel : ChannelInterface, user, items : List[OrderItemObject]) -> OrderResult:
    try:
        # 1. validate + price resolve
        resolved_items = []
        total = 0

        for item in items:
            variant = item.variant
            qty = item.quantity

            price = channel.get_price(variant=variant)
            InventoryService.reserve(variant=variant, quantity=qty)

            resolved_items.append((variant, qty, price))
            total += price * qty
        
        channel_obj,created = Channel.objects.get_or_create(code=channel.code , name=channel.plugin_name)

        # 2. create order
        order = Order.objects.create(
            channel=channel_obj,
            user=user,
            total=total,
        )

        for variant, qty, price in resolved_items:
            OrderItem.objects.create(
                order=order,
                variant=variant,
                quantity=qty,
                price=price,
            )

        # 3. emit event
        publish(OrdersCreated([order]))
        return OrderResult(success=True, order=order)

    except Exception as e:
        logger.error(e)
        return OrderResult(success=False, error=str(e))