from rest_framework.generics import ListAPIView
from . import serializers
from core.products.models import Product


class Menu(ListAPIView):
    serializer_class = serializers.ProductListSerializer

    def get_queryset(self):
        return Product.objects.all().order_by('title')
