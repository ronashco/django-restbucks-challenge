from rest_framework.generics import CreateAPIView, ListAPIView\
    , RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from ..models import Order
from .serializers import OrderListSerializer\
    , OrderCreateUpdateSerializer, UserCreateSerializer\
    , UserLoginSerializer

from .permissions import IsWaitingOrder, IsOwner

from django.contrib.auth import get_user_model


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


User = get_user_model()


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)