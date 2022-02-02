"""Data models for orders"""
import uuid
from django.db import models
from orders.constants import ORDER_STATUS
from products.mixins import ModelTimeBaseMixin


class OrderManager(models.Manager):
    """Manage order objects class"""
    def get_queryset(self):
        """Returns all orders that not canceled"""
        return super().get_queryset().exclude(status="Canceled")

class CanceledOrdersManager(models.Manager):
    """Manage order objects class"""
    def get_queryset(self):
        """Return all canceled_orders"""
        return super().get_queryset().filter(status='Canceled')

class Order(ModelTimeBaseMixin):
    """Order data model"""
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=32, choices=ORDER_STATUS, default="Waiting")
    total_price = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, null=True)
    
    objects = OrderManager()
    canceled_objects = CanceledOrdersManager()

class OrderItem(ModelTimeBaseMixin):
    """Order item data model"""
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    price = models.DecimalField(default=10.00, max_digits=10, decimal_places=2)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, null=True)
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, null=True)
    option = models.CharField(max_length=32, default="")


