from django.contrib import admin

from core.catalog.models import Category, Product

admin.site.register(Category)
admin.site.register(Product)
