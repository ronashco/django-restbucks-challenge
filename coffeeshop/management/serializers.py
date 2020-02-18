from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from coffeeshop.models import Product, CustomizableAttribute, CustomizableAttributeOption, Order, OrderItem


class CustomizableAttributeOptionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['name']
        model = CustomizableAttributeOption


class AttributeOptionWithAtrrNameSerializer(serializers.ModelSerializer):
    name = SerializerMethodField(source='attribute')
    value = serializers.CharField(source='name')

    class Meta:
        fields = ['name', 'value']
        model = CustomizableAttributeOption

    def get_name(self, obj):
        return obj.attribute.name


class CustomizableAttributeSerializer(serializers.ModelSerializer):
    options = SerializerMethodField()

    class Meta:
        fields = ['name', 'options']
        model = CustomizableAttribute

    def get_options(self, obj):
        return [opt.name for opt in obj.options.all()]


class ProductSerializer(serializers.ModelSerializer):
    attributes = CustomizableAttributeSerializer(source='customizable_attributes', many=True)

    class Meta:
        fields = ['product_name', 'unit_price', 'attributes']
        model = Product


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    selected_options = AttributeOptionWithAtrrNameSerializer(many=True)

    class Meta:
        exclude = ['order']
        model = OrderItem


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    customer = SerializerMethodField()

    class Meta:
        fields = ['id', 'customer', 'items', 'total_price', 'state']
        model = Order

    def get_customer(self, obj):
        return obj.customer.username
