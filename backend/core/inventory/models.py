from django.db import models
from core.catalog.models import Product

class Warehouse(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200, unique=True)
    
    def __str__(self):
        return self.name


class WarehouseLocation(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    code = models.CharField(max_length=50, unique=True) # like A-02-01
    description = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.code
    

class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE , related_name='stocks')
    location = models.ForeignKey(WarehouseLocation, on_delete=models.CASCADE, null=True , blank=True ,related_name='stocks')
    
    quantity = models.IntegerField()
    allocated = models.IntegerField(default=0)

    def get_available(self):
        return self.quantity - self.allocated
