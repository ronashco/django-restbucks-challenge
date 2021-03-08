from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
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
    # value_list = FeatureValueSerializer(many=True, read_only=True)
    # value_list = FeatureSerializer(many=True, read_only=True)

    class Meta:
        model = Feature
        fields = ('title', 'value_list')

    def get_value_list(self, obj):
        values = obj.featuresvalue_set.all()
        serialized_fv = FeatureValueSerializer(values, many=True, read_only=True).data
        return serialized_fv


class ProductSerializer(serializers.ModelSerializer):
    feature_list = FeatureWithValuesSerializer(read_only=True, many=True)
    consume_location = serializers.SerializerMethodField()
    # TODO: check standard serialize for choices

    class Meta:
        model = Product
        fields = ('id',
                  'title',
                  'cost',
                  'consume_location',
                  'feature_list')

    def get_consume_location(self, obj):
        return ConsumeLocation.types
