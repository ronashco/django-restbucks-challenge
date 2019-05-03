from rest_framework.serializers import ModelSerializer,SerializerMethodField

from .models import Product, ProductType, Order, OrderProduct, User, ProductOrderType


class ProductTypeSerializer(ModelSerializer):
    class Meta:
        model = ProductType
        fields = '__all__'


class ProductSerializer(ModelSerializer):
    type = ProductTypeSerializer(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)


class ProductOrderTypeSerializer(ModelSerializer):
    class Meta:
        model = ProductOrderType
        fields = '__all__'


class OrderProductSerializer(ModelSerializer):
    product_order_type = ProductOrderTypeSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderProduct
        fields = '__all__'


class OrderSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    items = SerializerMethodField()

    def get_items(self, obj):
        items = OrderProduct.objects.filter(order=obj, deleted=False)
        return OrderProductSerializer(items, many=True).data

    class Meta:
        model = Order
        fields = '__all__'

