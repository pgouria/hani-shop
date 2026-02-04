from datetime import timedelta
from unittest import mock

import jdatetime
from django.test import TestCase, SimpleTestCase
from django.utils import timezone

from .models import Digikala_Product, Digikala_Variant, Digikala_Order
from .tasks import fetch_orders


class DigikalaOrderModelTests(TestCase):
    def test_solar_dates_convert_from_gregorian(self):
        product = Digikala_Product.objects.create(
            product_id=1,
            category_id=10,
            title="Phone",
            image="https://example.com/phone.png",
        )
        variant = Digikala_Variant.objects.create(
            variant_id=100,
            seller_id=55,
            site="dk",
            is_active=True,
            is_archived=False,
            title="Phone Variant",
            product=product,
            shipping_type="fast",
            stock_in_digikala=5,
            stock_in_seller_warehouse=3,
            selling_stock=2,
            buy_box_price=0,
            is_buy_box_winner=True,
            fulfilment_and_delivery_cost=0,
            price=1000,
            selling_price=900,
            buying_price=800,
            commission_percentage=5,
        )
        created_at = timezone.now()
        commitment_date = created_at + timedelta(days=2)
        order = Digikala_Order.objects.create(
            order_item_id=123,
            order_id=456,
            variant=variant,
            product=product,
            quantity=1,
            order_status="new",
            shipment_status="pending",
            selling_price=900,
            created_at=created_at,
            commitment_date=commitment_date,
        )

        expected_created = jdatetime.datetime.fromgregorian(datetime=created_at)
        expected_commitment = jdatetime.datetime.fromgregorian(datetime=commitment_date)

        self.assertEqual(order.solar_created_at, expected_created)
        self.assertEqual(order.solar_commitment_date, expected_commitment)


class MarketplaceTasksTests(SimpleTestCase):
    def test_fetch_orders_calls_sync(self):
        with mock.patch(
            "backend.marketplace.digikala.application.sync_orders.sync_orders"
        ) as sync_mock:
            fetch_orders()

        sync_mock.assert_called_once()
