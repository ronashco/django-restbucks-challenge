from rest_framework.generics import ListAPIView
from . import serializers
from core.products.models import Product


class Menu(ListAPIView):
    serializer_class = serializers.ProductListSerializer
    queryset = Product.objects.all().order_by('title')
