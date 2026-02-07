from django.contrib import admin
from .models import Warehouse , WarehouseLocation , Stock

admin.site.register(Warehouse)
admin.site.register(WarehouseLocation)
admin.site.register(Stock)