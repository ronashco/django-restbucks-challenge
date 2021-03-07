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