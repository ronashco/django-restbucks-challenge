from rest_framework import serializers
from rest_framework.fields import SerializerMethodField, CharField, ReadOnlyField
from restbuck_app.models import *


class FeatureValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeaturesValue
        fields = ('id', 'title')


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ('title',)


class FeatureWithValuesSerializer(serializers.ModelSerializer):
    value_list = SerializerMethodField(read_only=True)

    class Meta:
        model = Feature
        fields = ('title', 'value_list')

    def get_value_list(self, obj):
        values = obj.featuresvalue_set.all()
        serialized_fv = FeatureValueSerializer(values, many=True, read_only=True).data
        return serialized_fv


class ProductSerializer(serializers.ModelSerializer):
    feature_list = FeatureWithValuesSerializer(read_only=True, many=True)
    consume_location = SerializerMethodField()
    # TODO: check standard serializer for choices

    class Meta:
        model = Product
        fields = ('id',
                  'title',
                  'cost',
                  'consume_location',
                  'feature_list')

    def get_consume_location(self, obj):
        return ConsumeLocation.types


class ProductOrderFlatSerializer(serializers.ModelSerializer):
    product_title = ReadOnlyField(source='product.title', read_only=True)
    consume_location_display = CharField(source='get_consume_location_display', read_only=True)
    feature_value_title = CharField(source='feature_value.title', read_only=True)

    class Meta:
        model = ProductOrder
        fields = ('product', 'product_title', 'count', 'consume_location', 'consume_location_display', 'feature_value',
                  'feature_value_title')


class OrderSerializer(serializers.ModelSerializer):
    product_list = ProductOrderFlatSerializer(source='productorder_set', read_only=True, many=True)
    status = CharField(source='get_status_display')

    class Meta:
        model = Order
        fields = ('id', 'status', 'product_list')