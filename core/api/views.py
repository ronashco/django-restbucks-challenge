from django.contrib.auth import authenticate
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from core.products.models import Product
from . import serializers


class Menu(ListAPIView):
    serializer_class = serializers.ProductListSerializer
    queryset = Product.objects.all().order_by('title')


@api_view(['POST'])
def register(request):
    serializer = serializers.RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'token': serializer.instance.auth_token.key},
                        status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    user = authenticate(username=request.data.get('email'),
                        password=request.data.get('password'))
    if user:
        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    else:
        return Response('Invalid credentials.', status=status.HTTP_400_BAD_REQUEST)
