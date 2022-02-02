"""API views to manipulate with products from UI server"""
from cgitb import lookup
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.db import transaction
from orders.models import Order
from orders.serializers import OrderSerializer, OrderUpdateSerializer, OrderCreateSerializer
from orders.custom_permissions import CustomPermissions

class OrderAPIView(ModelViewSet):
    """API View for order manipulaitons"""
    queryset = Order.objects.all()
    permission_classes = [CustomPermissions]
    serializer_class = OrderSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    pagination_class = None
    lookup_field = 'id'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user).order_by("-created_at")

    def get_serializer_class(self, *args, **kwargs):
        """Select serializer by action"""
        if self.action == 'create':
            return OrderCreateSerializer
        elif self.action == 'partial_update':
            return OrderUpdateSerializer
        return OrderSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """Create order object"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response("Created", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):
        """Update order"""
        order = Order.objects.get(id=kwargs.get("id"))
        if order.status == "Waiting":
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                instance = serializer.update(order, serializer.validated_data)
                return Response("Updated", status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response("Status of order must be waiting", status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        """Delete order"""
        order = Order.objects.get(id=kwargs.get("id"))
        if order.status == "Waiting":
            order.status = "Canceled"
            order.save()
            return Response("Order canceled", status=status.HTTP_200_OK)
        return Response("Status of order must be waiting", status=status.HTTP_400_BAD_REQUEST)