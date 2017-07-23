from rest_framework import serializers

from productions.api.serializers import MenuSerializer
from productions.models import Menu
from ..models import Order


class OrderListSerializer(serializers.ModelSerializer):
    ordered_productions = MenuSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'location',
            'address',
            'created_at',
            'updated_at',
            'ordered_productions',
            'status',
            'id'
        ]
        read_only_fields = [
            'status',
        ]


class OrderCreateUpdateSerializer(serializers.ModelSerializer):
    ordered_productions = MenuSerializer(many=True)

    def create(self, validated_data):
        ordered_productions_data = validated_data.pop("ordered_productions")
        order = Order.objects.create(**validated_data)
        for order_p_data in ordered_productions_data:
            Menu.objects.create(order=order, **order_p_data)
        return order

    class Meta:
        model = Order
        fields = [
            'location',
            'address',
            'created_at',
            'updated_at',
            'ordered_productions',
            'status',
            'id'
        ]
        read_only_fields = [
            'status',
        ]