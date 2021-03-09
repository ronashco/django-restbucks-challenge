from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from restbuck_app.models import *
from restbuck_app.serializers import *


class Menu(APIView):
    def get(self, request):
        products = Product.objects.all()
        data = []
        for product in products:
            data.append(ProductSerializer(product).data)
        return Response({'data': data,
                         'error': False})


def get_auth_user(request):
    return User.objects.get(id=1)


class MyOrders(APIView):
    def get(self, request):
        user = get_auth_user(request)
        orders = Order.objects.filter(user=user)
        data = []
        for order in orders:
            data.append(OrderSerializer(order).data)
        return Response({'data': data,
                         'error': False})
