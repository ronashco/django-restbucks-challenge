from rest_framework import serializers
from ..models import Menu, ProductOption, DetailOption


class DetailOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailOption
        fields = [
            'name'
        ]


class ProductOptionSerializer(serializers.ModelSerializer):
    detail_option = DetailOptionSerializer(many=True)

    class Meta:
        model = ProductOption
        fields = [
            'name',
            'detail_option'
        ]


class MenuSerializer(serializers.ModelSerializer):
    options = ProductOptionSerializer(many=True)

    class Meta:
        model = Menu
        fields = [
            'name',
            'options',
            'price'
        ]

