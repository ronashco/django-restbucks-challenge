from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, DestroyAPIView, CreateAPIView, ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from core.products.models import Product
from core.orders import utils
from core.orders.models import Cart, CartApiModel, Order, OrderProductApiModel
from . import serializers


class Menu(ListAPIView):
    """
    Return a list of all existing products.
    """
    serializer_class = serializers.ProductListSerializer
    queryset = Product.objects.all().order_by('title')


@api_view(['POST'])
def register(request):
    """
    Store user in database and return associated token key.
    :param request:
    :return:
    """
    serializer = serializers.RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'token': serializer.instance.auth_token.key},
                        status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    """
    Return user token, if requested data is valid.
    :param request:
    :return:
    """
    user = authenticate(username=request.data.get('email'),
                        password=request.data.get('password'))
    if user:
        try:
            token = Token.objects.get(user=user)
        # if user doesnt have token, we will create one.
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    else:
        return Response('Invalid credentials.', status=status.HTTP_400_BAD_REQUEST)


class CartView(RetrieveAPIView, CreateAPIView, DestroyAPIView):
    """
    get:
    Return user cart.

    post:
    Add item to the user cart.

    delete:
    Remove item from cart.
    """
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        # We use core.api.serializers.ShowCartsSerializer to retrieve data,
        # for any other purpose (create/delete/...) we use core.api.serializers.CartSerializer.
        if self.request.method == 'GET':
            return serializers.ShowCartsSerializer
        return serializers.CartSerializer

    def get_object(self):
        if self.request.method == 'GET':
            # We use core.carts.models.CartApiModel as a model for core.api.serializers.CartSerializer to
            # retrieve cart data
            user = self.request.user
            qs = Cart.objects.select_related('product').filter(user=user).order_by('-create_date')
            return CartApiModel(*utils.user_cart_detail(qs))
        else:
            # for any other purpose we use core.carts.models.Cart (primary cart model)
            return get_object_or_404(Cart, product_id=self.request.data.get('product'),
                                     user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(status=status.HTTP_201_CREATED, headers=headers)


class OrderListCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.OrderListSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-date')

    def get_serializer(self, *args, **kwargs):
        if self.request.method == 'POST':
            """
            in POST requests, we want to just store an order object and return it.
            so we wont to return a list of objects.
            """
            kwargs.update({'many': False})
        return super(OrderListCreateView, self).get_serializer(*args, **kwargs)

    def perform_create(self, serializer):
        order = serializer.save(user=self.request.user, total_price=False)
        total_price, order_products = utils.merge_cart_to_order(order)
        serializer.save(total_price=total_price)


class OrderView(RetrieveUpdateDestroyAPIView):
    """
    get:
    Return order data with associated products.

    patch/put:
    Update a waiting order.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.OrderSerializer

    def get_object(self):
        kwargs = dict(user=self.request.user, id=self.kwargs['order_id'])
        if self.request.method == 'GET':
            # We need to fetch related products too.
            queryset = Order.objects.prefetch_related('orderproduct_set',
                                                      'orderproduct_set__product')
            order = get_object_or_404(queryset, **kwargs)
            order.order_products = self._get_order_products(order.orderproduct_set.all())
            return order
        elif self.request.method == 'DELETE':
            kwargs.update({'status': 'w'})
            return get_object_or_404(Order, **kwargs)
        else:
            # For edit/delete purpose, only order object (with anymore related objects) is enough.
            return get_object_or_404(Order, **kwargs)

    @staticmethod
    def _get_order_products(order_products_query_set):
        # A helper method to fetch product data.
        return [OrderProductApiModel(title=op.product.title,
                                     price=op.price,
                                     option=op.product.option,
                                     item=op.customization,
                                     id_=op.product.id)
                for op in order_products_query_set]
