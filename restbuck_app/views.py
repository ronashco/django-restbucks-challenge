from rest_framework import status
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


class OrderView(APIView):
    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            raise Http404

    def get(self, request, pk=0):
        user = get_auth_user(request)
        if pk != 0:
            order = self.get_object(pk)
            if order.user != user:
                return Response({'error': True, 'message': 'not your order'}, status=status.HTTP_403_FORBIDDEN)
            data = OrderSerializer(order).data
        else:
            orders = Order.objects.filter(user=user)
            data = []
            for order in orders:
                data.append(OrderSerializer(order).data)
        return Response({'data': data,
                         'error': False})
