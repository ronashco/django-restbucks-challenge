from rest_framework.generics import ListAPIView

from ..models import Menu
from serializers import MenuSerializer


class MenuListAPIVeiw(ListAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


