from rest_framework.serializers import ModelSerializer
from core.products.models import Product


class ProductListSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ('title', 'price', 'option', 'items')
