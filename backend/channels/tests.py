from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch

from channels.plugin import WebSiteChannelPlugin
from shop.models import Category, Product, Variant


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


class WebSiteChannelPluginTests(TestCase):
    def setUp(self):
        self.plugin = WebSiteChannelPlugin()
        self.variant = _make_variant()

    def test_get_price_uses_variant_base_price(self):
        price = self.plugin.get_price(variant=self.variant)
        self.assertEqual(price, self.variant.base_price)

    def test_is_available_true_when_stock_positive(self):
        with patch("channels.plugin.InventoryService.get_stock", return_value=5):
            self.assertTrue(self.plugin.is_available(variant=self.variant))

    def test_is_available_false_when_stock_zero(self):
        with patch("channels.plugin.InventoryService.get_stock", return_value=0):
            self.assertFalse(self.plugin.is_available(variant=self.variant))

    def test_get_stock_proxies_to_inventory_service(self):
        with patch("channels.plugin.InventoryService.get_stock", return_value=3) as get_stock:
            result = self.plugin.get_stock(variant=self.variant)

        self.assertEqual(result, 3)
        get_stock.assert_called_once_with(variant=self.variant)

# Create your tests here.
