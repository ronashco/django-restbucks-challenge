from django.contrib.auth import authenticate
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from core.products.models import Product
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
