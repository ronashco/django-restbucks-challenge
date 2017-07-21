from rest_framework import serializers
from rest_framework.utils.representation import manager_repr

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

    # def get_detail_option(self, obj):
    #     d_qs = DetailOption.objects.filter_by_instance(obj)
    #     details = DetailOptionSerializer(d_qs, many=True).data
    #     return details


class MenuSerializer(serializers.ModelSerializer):
    options = ProductOptionSerializer(many=True)

    class Meta:
        model = Menu
        fields = [
            'name',
            'options',
            'price'
        ]

    # def get_options(self, obj):
    #     o_qs = ProductOption.objects.filter_by_instance(obj)
    #     options = ProductOptionSerializer(o_qs, many=True).data
    #     return options
