from django.contrib import admin
from products.models import Product, AvailableProductOption

admin.site.register(Product)
admin.site.register(AvailableProductOption)
