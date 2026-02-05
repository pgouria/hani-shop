from django.db import models
from shop.models import Product

class Channel(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name
    
class ProductChannel(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='channels')
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE,related_name='products')

   
    is_published = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ('product', 'channel')
