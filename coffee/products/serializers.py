"""Serializers for product API"""
from rest_framework import serializers

from products.models import Product, AvailableProductOption

class AvailableProductOptionSerializer(serializers.ModelSerializer):
    """Display options for product"""
    class Meta:
        model = AvailableProductOption
        fields = ("id",
                  "name",
                  "option",)

class ProductSerializer(serializers.ModelSerializer):
    """Display all kind of products with their options"""
    availableproductoption_set = AvailableProductOptionSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = ("id",
                  "name",
                  "availableproductoption_set")
