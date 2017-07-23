from rest_framework import serializers

from productions.api.serializers import MenuSerializer
from ..models import Order


class OrderSerializer(serializers.ModelSerializer):
    ordered_productions = MenuSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'location',
            'address',
            'created_at',
            'updated_at',
            'ordered_productions',
            'status',
        ]
        read_only_fields = [
            'status',
        ]

