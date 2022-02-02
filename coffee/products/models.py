"""Data models for products"""
import uuid
from django.db import models
from products.constants import (MILK_OPTIONS, PRODUCT_NAMES, OPTION_NAMES,
                                SIZE_TYPE, SHOT_OPTIONS, OPSTIONS,
                                KIND_OF_COOKIE, LOCATION_OPTION)
from products.mixins import ModelTimeBaseMixin

class Product(ModelTimeBaseMixin):
    """Product data model"""
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=512, choices=PRODUCT_NAMES, null=True, blank=True)
    # milk_option = models.CharField(max_length=512, choices=MILK_OPTIONS, null=True, blank=True)
    # size_option = models.CharField(max_length=512, choices=SIZE_TYPE, null=True, blank=True)
    # shot_quantity = models.CharField(max_length=512, choices=SHOT_OPTIONS, null=True, blank=True)
    # kind_of_cookie = models.CharField(max_length=512, choices=KIND_OF_COOKIE, null=True, blank=True)
    # pickup_method = models.CharField(max_length=512, choices=LOCATION_OPTION, null=True, blank=True)

    price = models.DecimalField(default=10.00, max_digits=10, decimal_places=2)


    def __str__(self):
        return f"{self.name}"

class AvailableProductOption(ModelTimeBaseMixin):
    """Product data model"""
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=512, choices=OPTION_NAMES, null=True, blank=True)
    option = models.CharField(max_length=512, choices=OPSTIONS, null=True, blank=True)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, null=True)
    price = models.DecimalField(default=1.50, max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name}"