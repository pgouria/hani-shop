from django.contrib import admin
from .models import Product , Variant , Order
# Register your models here.

admin.site.register(Product)
admin.site.register(Variant)
admin.site.register(Order)
