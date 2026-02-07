from django.db import models
from shop.models import Variant

class Channel(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name
    
class VariantChannel(models.Model):
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE,related_name='channels')
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE,related_name='variants')

    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    is_published = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ('variant', 'channel')
