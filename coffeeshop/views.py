import os
import stat
from tempfile import NamedTemporaryFile

from celery.result import AsyncResult
from django.conf import settings
from django.http import FileResponse, HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.encoding import smart_str
from django_fsm import can_proceed
from rest_framework import generics, status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from coffeeshop.management.serializers import ProductSerializer, OrderSerializer
from coffeeshop.models import Product, Order
from .tasks import create_order


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)


class CreateOrderView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        order = request.data.get("order")
        if order:
            create_order.apply_async(kwargs={'user_id': request.user.id, 'items': order})
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserOrdersView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        queryset = self.get_queryset()
        user_orders = queryset.filter(customer=request.user).all()
        serializer = self.get_serializer_class()
        return Response(serializer(user_orders, many=True).data)


class CancelOrderView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        order_id = request.data.get("order_id")
        if str(order_id).isnumeric():
            order = Order.objects.filter(pk=order_id, customer=request.user).first()
            if order and can_proceed(order.cancel):
                order.cancel()
                order.save()
                return Response(status=status.HTTP_200_OK)
            elif not can_proceed(order.cancel):
                return Response({"fault_error": "only waiting orders can be canceled"},
                                status=status.HTTP_403_FORBIDDEN)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class EditOrderView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        order = request.data.get("order")
        order_id = request.data.get("order_id")
        if order and Order.objects.filter(customer=request.user.id, pk=order_id).exists():
            Order.objects.filter(customer=request.user.id, pk=order_id).delete()
            create_order.apply_async(kwargs={'user_id': request.user.id, 'items': order})
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
