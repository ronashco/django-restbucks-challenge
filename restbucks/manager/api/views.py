from manager.api.serializers import (ProductListSerializer,
                                     OrderCreateSerializer,
                                     OrderDetailSerializer,
                                     OrderDeleteSerializer,
                                     OrderUpdateSerializer,)
from manager.models import Product,Order
from rest_framework import generics
from django.core.exceptions import PermissionDenied
from .permissions import OwnerCanManageOrReadOnly



class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer


class OrderCreateAPIView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer


class OrderDetailAPIView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    lookup_field = 'customer'



    ##########################

class OrderDeleteAPIView(generics.RetrieveDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderDeleteSerializer
    # permission_classes = (OwnerCanManageOrReadOnly,)
    lookup_field = 'id'

    # def perform_destroy(self, serializer):
    #     # just owner can delete post
    #     if serializer.owner != self.request.user:
    #         raise PermissionDenied
    #     else:
    #         serializer.delete()
    #         # you can send email here and etc. this email send when serializer delete


class OrderUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderUpdateSerializer
    # permission_classes = (OwnerCanManageOrReadOnly,)
    lookup_field = 'id'
    #
    # def perform_update(self, serializer):
    #     serializer.save(owner=self.request.user)
    #     # you can send email here and etc. this email send when serializer update

