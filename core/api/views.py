from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from . import serializers
from core.products.models import Product


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
