from django.contrib import admin

from .models import *

admin.site.register(Product)
admin.site.register(ProductType)
admin.site.register(ProductOrderType)
admin.site.register(Order)
admin.site.register(OrderProduct)

