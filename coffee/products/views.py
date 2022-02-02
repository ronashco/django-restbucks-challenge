"""API views to manipulate with products from UI server"""
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from products.models import Product
from products.serializers import ProductSerializer

# Create your views here.
class ProductsAPIView(ModelViewSet):
    """API View for product manipulaitons"""
    queryset = Product.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
    http_method_names = ['get']
    pagination_class = None

    def get_queryset(self):
        return super().get_queryset().filter()
