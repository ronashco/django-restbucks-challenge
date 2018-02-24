from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.http.request import QueryDict
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, DestroyAPIView, CreateAPIView
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from core.products.models import Product
from core.orders.utils import user_cart_detail
from core.orders.models import Cart, CartApiModel
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
            return CartApiModel(*user_cart_detail(qs))
        else:
            # for any other purpose we use core.carts.models.Cart (primary cart model)
            return get_object_or_404(Cart, product_id=self.request.data.get('product'),
                                     user=self.request.user)

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, QueryDict):
            user = request.user

            # In some cases like get requests or requests without data,
            # request.data will be dict instance then following code
            # causes exception. We must make sure request.data is instance of QueryDict

            request.data._mutable = True
            request.data.update({'user': user.id})

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)

        return Response(status=status.HTTP_201_CREATED, headers=headers)
