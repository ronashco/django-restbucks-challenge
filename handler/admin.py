from django.contrib import admin
from .models import Product , OrderStatus , Order
# Register your models here.

admin.site.register(Product)
admin.site.register(OrderStatus)
admin.site.register(Order)