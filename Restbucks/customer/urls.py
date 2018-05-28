from django.urls import path
from .views import *
from django.conf.urls import url, include

urlpatterns = [
    path('', MainPageView, name='main_page'),

    path('neworder/', NewOrderView.as_view(), name='neworder'),

    path('orders/', ShowOrders, name=('orders')),
    path('change/<ID_num>/', ChangeOrder.as_view(), name='change'),
    path('cancle/<ID_num>/', CancleOrder, name='cancle')


]