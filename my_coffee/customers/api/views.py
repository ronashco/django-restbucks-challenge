from rest_framework.generics import CreateAPIView, ListAPIView\
    , RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from ..models import Order
from .serializers import OrderListSerializer\
    , OrderCreateUpdateSerializer
from .permissions import IsWaitingOrder, IsOwner


class OrderCreateAPIView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class OrderListAPIView(ListAPIView):
    serializer_class = OrderListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset_list = Order.objects.filter(owner=self.request.user)
        return queryset_list


class OrderUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateUpdateSerializer
    lookup_field = 'id'
    permission_classes = [
        IsAuthenticated,
        IsOwner,
        IsWaitingOrder
    ]

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)


class OrderDeleteAPIView(DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateUpdateSerializer
    lookup_field = 'id'
    permission_classes = [
        IsAuthenticated,
        IsOwner,
        IsWaitingOrder
    ]