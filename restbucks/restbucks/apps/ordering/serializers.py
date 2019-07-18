from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Product, OptionSet, Option, Order, OrderItem


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'value']


class OptionSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionSet
        fields = ['id', 'name', 'options']

    options = OptionSerializer(many=True)


class ProductMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'option_sets']

    option_sets = OptionSetSerializer(many=True)


##
class OptionOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id']


class OptionSetOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionSet
        fields = ['id']


class OrderItemsSerializer(serializers.Serializer):
    class Meta:
        fields = ['product_id', 'option_set_id', 'option_id']

    product_id = serializers.IntegerField()
    option_set_id = serializers.IntegerField(required=False)
    option_id = serializers.IntegerField(required=False)

    def validate(self, attrs):
        from .services import ProductService
        validated_data = super(OrderItemsSerializer, self).validate(attrs)
        try:
            product = ProductService.get(id=validated_data['product_id'])
        except Product.DoesNotExist:
            raise ValidationError(_('Invalid Product Id'))

        if validated_data.get('option_set_id') and validated_data.get('option_id'):
            try:
                option_set = ProductService.get_option_set(id=validated_data['option_set_id'])
            except OptionSet.DoesNotExist:
                raise ValidationError(_('Invalid Option-Set Id'))
            try:
                option = ProductService.get_option(id=validated_data['option_id'])
            except Option.DoesNotExist:
                raise ValidationError(_('Invalid Option Id'))

            if option.option_set != option_set:
                raise ValidationError(_('Invalid Option Id'))

        return validated_data


class RegisterOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['items', 'consume_location', 'delivery_address']

    items = OrderItemsSerializer(many=True)

    def validate(self, attrs):
        validated_data = super(RegisterOrderSerializer, self).validate(attrs)
        if validated_data['consume_location'] == 'out' \
           and not validated_data['delivery_address']:
            raise ValidationError(_('The "address" field must not be empty'))
        return validated_data

    def update(self, order, attrs):
        from .services import ProductService, OrderService

        with transaction.atomic():
            # Undo all DB queries if an exception occured
            order.consume_location = attrs['consume_location']
            order.delivery_address = attrs['delivery_address']
            order.save()
            for item_info in attrs.get('items', []):
                try:
                    product = ProductService.get(id=item_info['product_id'])
                    option_set = None
                    option = None
                    if item_info.get('option_set_id') and item_info.get('option_id'):
                        option_set = ProductService.get_option_set(id=item_info['option_set_id'])
                        option = ProductService.get_option(id=item_info['option_id'])
                except Exception:
                    raise ValidationError(_('Entered Values Is Not Acceptable'))
                OrderService.add_item(order, product, option_set, option)
            order.save()

        return order

##


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'option_set', 'option']

    product = ProductSerializer()
    option_set = OptionSetSerializer()
    option = OptionSerializer()


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'items', 'consume_location', 'delivery_address']

    items = OrderItemSerializer(many=True)

    # products = OrderItemsSerializer(many=True)


##


class StatusSerializer(serializers.Serializer):
    class Meta:
        fields = ['status']

    status = serializers.ChoiceField(choices=Order.STATUS_CHOICES)
