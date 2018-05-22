from manager.models import Product
from rest_framework.serializers import (
    ModelSerializer,
)


############ PRODUCT SERIALIZERS ############
class ProductListSerializer(ModelSerializer):
    class Meta:
        model=Product
        fields='__all__'

class ProductCreateSerializer(ModelSerializer):
      class Meta:
         model = Product
         fields = '__all__'

############ ORDER SERIALIZERS ############
