"""Serializers for product API"""
from ast import Or
from math import prod
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from orders.models import Order, OrderItem
from products.models import AvailableProductOption, Product


class OrderItemProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ("id", "name")

class OrderItemSerializer(serializers.ModelSerializer):
    product = OrderItemProductSerializer()
    class Meta:
        model = OrderItem
        fields = ("id", "product", "option")


class OrderSerializer(serializers.ModelSerializer):
    orderitem_set = OrderItemSerializer(read_only=True, many=True)
    class Meta:
        model = Order
        fields = ("id", "status", "total_price", "orderitem_set")


class OrderUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields = ("status",)

    def update(self, instance, validated_data):
        """Update order"""
        instance.status = validated_data.get("status")
        instance.save()
        return "Done"


class OrderItemCreateSerializer(serializers.ModelSerializer):
    product_id = serializers.CharField()
    class Meta:
        model = OrderItem
        fields = ("product_id", "option",)


class OrderCreateSerializer(serializers.ModelSerializer):
    order_items = OrderItemCreateSerializer( many=True)
    class Meta:
        model = Order
        fields = ("order_items",)

    def validate(self, attrs):
        """Validate fields and values"""
        for attr in attrs.get("order_items"):
            available_list = AvailableProductOption.objects.filter(
                                                product=attr.get("product_id")).values_list(
                                                                                "option", flat=True)
            if attr.get("option") not in available_list:
                raise ValidationError(f"Option not available for this product - {available_list}")
        return super().validate(attrs)

    def create(self, validated_data):
        """Create order function"""
        order = Order.objects.create(user=self.context['request'].user)
        for item in validated_data.get("order_items"):
            product = Product.objects.get(id=item.get("product_id"))
            item["order"] = order
            item["price"] = float(product.price) + float(AvailableProductOption.objects.get(
                                                product=item.get("product_id"),
                                                option=item.get("option")).price)
            OrderItem.objects.create(**item)
            order.total_price = float(order.total_price) + item["price"]
        order.save()
        return order
