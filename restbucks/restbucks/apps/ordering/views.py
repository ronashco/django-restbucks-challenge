from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status

from .serializers import ProductMenuSerializer, OrderSerializer, RegisterOrderSerializer, \
    StatusSerializer
from .services import ProductService, OrderService


class OrderingMenuAPIView(APIView):
    http_method_names = ['get']

    def get_queryset(self):
        return ProductService.fetch_menu_list()

    def get_serializer_class(self):
        return ProductMenuSerializer

    def get(self, request):
        products = self.get_queryset()
        SerializerClass = self.get_serializer_class()
        serializer = SerializerClass(products, many=True)
        return Response(serializer.data)


class OrderingAPIView(CreateModelMixin, ListModelMixin, APIView):
    http_method_names = ['get', 'post']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.method.lower() == 'post':
            order = OrderService.create_order_on_the_fly()
            order.client = self.request.user
            return order
        return OrderService.all_orders_of(self.request.user)

    def get_serializer_class(self):
        if self.request.method.lower() == 'post':
            return RegisterOrderSerializer
        return OrderSerializer

    def post(self, request):
        order = self.get_queryset()
        SerializerClass = self.get_serializer_class()
        serializer = SerializerClass(instance=order, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = dict(serializer.data)
        data.update(id=serializer.instance.id)
        return Response(data, status=status.HTTP_201_CREATED)

    def get(self, request):
        products = self.get_queryset()
        SerializerClass = self.get_serializer_class()
        serializer = SerializerClass(products, many=True)
        return Response(serializer.data)


class OrderingDeleteUpdateAPIView(UpdateModelMixin, DestroyModelMixin, APIView):
    http_method_names = ['put', 'delete']
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return OrderService.get(self.request.user)

    def put(self, request, pk):
        serializer = StatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        OrderService.update_status(pk, status)
        return Response({}, status.HTTP_202_ACCEPTED)

    def delete(self, request, pk):
        order = OrderService.get(id=pk)
        OrderService.delete(order)
        return Response({}, status.HTTP_204_NO_CONTENT)
