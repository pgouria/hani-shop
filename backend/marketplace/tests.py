from .tasks import fetch_orders
from django.test import SimpleTestCase
from unittest import mock

class MarketplaceTasksTests(SimpleTestCase):
    def test_fetch_orders_calls_sync(self):
        with mock.patch(
            "marketplace.digikala.application.sync_orders.sync_orders"
        ) as sync_mock:
            fetch_orders()

        sync_mock.assert_called_once()
