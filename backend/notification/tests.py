from types import SimpleNamespace
from unittest import mock

from django.test import SimpleTestCase

from . import handlers
from .plugins import telegram as telegram_plugin


class NotificationHandlerTests(SimpleTestCase):
    def test_on_orders_created_sends_orders(self):
        fake_event = SimpleNamespace(orders=["order-1", "order-2"])

        with mock.patch.object(handlers, "send_orders_notification") as send_mock:
            handlers.on_orders_created(fake_event)

        send_mock.assert_called_once_with(fake_event.orders)


class TelegramPluginTests(SimpleTestCase):
    def test_send_orders_notification_formats_message(self):
        order_a = SimpleNamespace(order_id=101, variant=SimpleNamespace(title="Widget"))
        order_b = SimpleNamespace(order_id=202, variant=SimpleNamespace(title="Gadget"))

        with mock.patch.object(telegram_plugin, "_send", new_callable=mock.AsyncMock) as send_mock, \
             mock.patch.object(telegram_plugin.asyncio, "run") as run_mock:

            telegram_plugin.send_orders_notification([order_a, order_b])

        run_mock.assert_called_once()

        message = send_mock.call_args[0][0]
        self.assertIn("🛒 New Orders:", message)
        self.assertIn("- 101 | Widget", message)
        self.assertIn("- 202 | Gadget", message)

