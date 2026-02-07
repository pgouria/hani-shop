from django.db import models

from accounts.models import User
from shop.models import   Variant
from channels.models import Channel

class OrderStatus(models.TextChoices):
    PENDING = 'PENDING'
    PAID = 'PAID'
    SHIPPED = 'SHIPPED'
    DELIVERED = 'DELIVERED'
    CANCELLED = 'CANCELLED'

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    channel = models.ForeignKey(Channel, on_delete=models.PROTECT, related_name='orders')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f"{self.user.full_name} - order id: {self.id}"

    @property
    def get_total_price(self):
        total = sum(item.get_cost() for item in self.items.all())
        return total
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    variant = models.ForeignKey(Variant, on_delete=models.PROTECT, related_name='order_items')
    price = models.IntegerField()
    quantity = models.SmallIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity