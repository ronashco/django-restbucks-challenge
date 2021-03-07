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


class ProductSerializer(serializers.ModelSerializer):
    feature_list = FeatureWithValuesSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = ('id',
                  'title',
                  'cost',
                  'feature_list')