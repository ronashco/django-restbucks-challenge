from manager.models import Product,Order
from rest_framework.serializers import (
    ModelSerializer,
)


############ PRODUCT SERIALIZERS ############
class ProductListSerializer(ModelSerializer):
    class Meta:
        model=Product
        fields='__all__'


############ ORDER SERIALIZERS ############
class OrderDetailSerializer(ModelSerializer):
    class Meta:
        model=Order
        fields='__all__'


class OrderCreateSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_field = ['status']

######################################

class OrderDeleteSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderUpdateSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'