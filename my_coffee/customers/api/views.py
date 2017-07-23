from rest_framework.generics import CreateAPIView, ListAPIView

from ..models import Order
from .serializers import OrderSerializer


class OrderCreateAPIView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class OrderListAPIView(ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset_list = Order.objects.filter(owner=self.request.user)
        return queryset_list

