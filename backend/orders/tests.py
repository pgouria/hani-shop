from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch
import types

from accounts.models import User
from channels.models import Channel
from orders.models import Order, OrderItem
from orders.services import place_order
from shop.models import Category, Product, Variant
from core.domain.orders import OrdersCreated


def _make_variant():
    category = Category.objects.create(title="Cat", slug="cat")
    image = SimpleUploadedFile("test.jpg", b"file", content_type="image/jpeg")
    product = Product.objects.create(
        category=category,
        image=image,
        title="Prod",
        description="Desc",
        slug="prod",
    )
    return Variant.objects.create(product=product, sku="sku-1", base_price=10)


class OrderServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@example.com",
            full_name="User Test",
            password="password123",
        )
        self.variant = _make_variant()
        self.channel = Channel.objects.create(name="Web", code="web")

        def _get_price(self, *, variant, **kwargs):
            return 10

        self.channel.get_price = types.MethodType(_get_price, self.channel)

    def test_place_order_success_creates_order_and_items(self):
        items = [{"variant": self.variant, "quantity": 2}]

        with patch("orders.services.InventoryService.reserve") as reserve, \
             patch("orders.services.publish") as publish:
            result = place_order(channel=self.channel, user=self.user, items=items)

        self.assertTrue(result.success)
        self.assertIsNotNone(result.order)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 1)

        order = result.order
        self.assertEqual(order.total, 20)
        self.assertTrue(order.status)

        item = order.items.first()
        self.assertEqual(item.variant, self.variant)
        self.assertEqual(item.quantity, 2)
        self.assertEqual(item.price, 10)

        reserve.assert_called_once_with(variant=self.variant, quantity=2)
        publish.assert_called_once()
        event = publish.call_args.args[0]
        self.assertIsInstance(event, OrdersCreated)
        self.assertEqual(event.orders, [order])

    def test_place_order_returns_error_on_exception(self):
        items = [{"variant": self.variant, "quantity": 2}]

        with patch("orders.services.InventoryService.reserve", side_effect=Exception("Boom")):
            result = place_order(channel=self.channel, user=self.user, items=items)

        self.assertFalse(result.success)
        self.assertEqual(result.error, "Boom")
        self.assertEqual(Order.objects.count(), 0)
