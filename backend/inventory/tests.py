from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import Mock

from core.plugins.registry import registry
from inventory.services import InventoryService, _get_available_stocks, _get_allocated_stocks
from inventory.plugin import WarehousePlugin
from inventory.models import Stock
from shop.models import Category, Product, Variant
from inventory.models import Warehouse, WarehouseLocation


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


class InventoryServiceTests(TestCase):
    def setUp(self):
        self._original_inventory = list(registry.inventory)

    def tearDown(self):
        registry.inventory = self._original_inventory

    def test_reserve_returns_when_plugin_handles(self):
        plugin = Mock()
        plugin.reserve = Mock(return_value=True)
        registry.inventory = [plugin]

        InventoryService.reserve(variant="v1", quantity=2)

        plugin.reserve.assert_called_once_with(variant="v1", quantity=2)

    def test_reserve_raises_when_no_plugin_handles(self):
        plugin = Mock()
        plugin.reserve = Mock(return_value=False)
        registry.inventory = [plugin]

        with self.assertRaises(Exception) as ctx:
            InventoryService.reserve(variant="v1", quantity=2)

        self.assertIn("No inventory plugin handled reservation", str(ctx.exception))

    def test_get_stock_returns_first_plugin_value(self):
        plugin = Mock()
        plugin.get_stock = Mock(return_value=7)
        registry.inventory = [plugin]

        result = InventoryService.get_stock(variant="v1")

        self.assertEqual(result, 7)
        plugin.get_stock.assert_called_once_with(variant="v1")


class InventoryHelpersTests(TestCase):
    def setUp(self):
        self.variant = _make_variant()
        self.location = WarehouseLocation.objects.create(
            warehouse=Warehouse.objects.create(name="W1", code="w1"),
            code="A-01",
        )

    def test_get_available_stocks_returns_all_for_variant(self):
        Stock.objects.create(variant=self.variant, location=self.location, quantity=5, allocated=2)
        Stock.objects.create(variant=self.variant, location=self.location, quantity=3, allocated=0)

        stocks = _get_available_stocks(self.variant)

        self.assertEqual(len(stocks), 2)

    def test_get_allocated_stocks_filters_allocated(self):
        Stock.objects.create(variant=self.variant, location=self.location, quantity=5, allocated=2)
        Stock.objects.create(variant=self.variant, location=self.location, quantity=3, allocated=0)

        stocks = _get_allocated_stocks(self.variant)

        self.assertEqual(len(stocks), 1)
        self.assertEqual(stocks[0].allocated, 2)


class WarehousePluginTests(TestCase):
    def setUp(self):
        self.variant = _make_variant()
        self.location = WarehouseLocation.objects.create(
            warehouse=Warehouse.objects.create(name="W1", code="w1"),
            code="A-01",
        )
        self.plugin = WarehousePlugin()

    def test_reserve_allocates_across_stocks(self):
        s1 = Stock.objects.create(variant=self.variant, location=self.location, quantity=5, allocated=0)
        s2 = Stock.objects.create(variant=self.variant, location=self.location, quantity=3, allocated=0)

        self.plugin.reserve(variant=self.variant, quantity=6)

        s1.refresh_from_db()
        s2.refresh_from_db()
        self.assertEqual(s1.allocated, 5)
        self.assertEqual(s2.allocated, 1)

    def test_reserve_raises_when_insufficient(self):
        Stock.objects.create(variant=self.variant, location=self.location, quantity=2, allocated=0)

        with self.assertRaises(Exception) as ctx:
            self.plugin.reserve(variant=self.variant, quantity=5)

        self.assertIn("Not enough stocks", str(ctx.exception))

    def test_release_deallocates(self):
        s1 = Stock.objects.create(variant=self.variant, location=self.location, quantity=5, allocated=3)
        s2 = Stock.objects.create(variant=self.variant, location=self.location, quantity=3, allocated=2)

        self.plugin.release(variant=self.variant, quantity=4)

        s1.refresh_from_db()
        s2.refresh_from_db()
        self.assertEqual(s1.allocated + s2.allocated, 1)

    def test_commit_decreases_quantity_and_allocated(self):
        s1 = Stock.objects.create(variant=self.variant, location=self.location, quantity=5, allocated=3)

        self.plugin.commit(variant=self.variant, quantity=2)

        s1.refresh_from_db()
        self.assertEqual(s1.allocated, 1)
        self.assertEqual(s1.quantity, 3)

    def test_get_stock_returns_total_available(self):
        Stock.objects.create(variant=self.variant, location=self.location, quantity=5, allocated=2)
        Stock.objects.create(variant=self.variant, location=self.location, quantity=3, allocated=0)

        total = self.plugin.get_stock(variant=self.variant)

        self.assertEqual(total, 6)
