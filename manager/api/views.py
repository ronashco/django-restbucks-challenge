from manager.api.serializers import ProductListSerializer, ProductCreateSerializer
from manager.models import Product
from rest_framework import generics


class ProductListAPIView(generics.ListAPIView): # inja az anva bayad estefade kard
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer



class ProductCreateAPIView(generics.CreateAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
