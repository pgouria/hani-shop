from django.db import models
import jdatetime
from shop.models import Variant as VariantModel

class Product(models.Model):
    external_product_id = models.IntegerField(unique=True)
    category_id = models.IntegerField()
    title = models.CharField(max_length=255)
    image = models.URLField(default="#")

 
class Variant(models.Model):
    linked_variant = models.ForeignKey(VariantModel, on_delete=models.CASCADE)
    external_variant_id = models.IntegerField()
    seller_id = models.IntegerField()
    site = models.CharField(max_length=50)
    is_active = models.BooleanField()
    is_archived = models.BooleanField()
    title = models.CharField(max_length=255)
    external_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    shipping_type = models.CharField(max_length=50)
    stock_in_digikala = models.IntegerField()
    stock_in_seller_warehouse = models.IntegerField()
    selling_stock = models.IntegerField()
    buy_box_price = models.DecimalField(max_digits=10, decimal_places=2,default=0,null=True)
    is_buy_box_winner = models.BooleanField(null=True)
    fulfilment_and_delivery_cost = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    buying_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    commission_percentage = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    
    

class Order(models.Model):
    order_item_id = models.IntegerField()
    order_id = models.IntegerField()
    external_variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    external_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    order_status = models.CharField(max_length=50)
    shipment_status = models.CharField(max_length=50)
    selling_price = models.FloatField()
    created_at = models.DateTimeField()
    commitment_date = models.DateTimeField()

      
    @property
    def solar_created_at(self):
        return jdatetime.datetime.fromgregorian(datetime=self.created_at)

    @property
    def solar_commitment_date(self):
        return jdatetime.datetime.fromgregorian(datetime=self.commitment_date)
