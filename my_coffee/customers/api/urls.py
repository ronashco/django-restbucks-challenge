from django.conf.urls import include, url
from views import OrderCreateAPIView, OrderListAPIView\
    , OrderUpdateAPIView, OrderDeleteAPIView


urlpatterns = [
    url(r'^$', OrderListAPIView.as_view(), name="order"),
    url(r'^order/$', OrderListAPIView.as_view(), name="order"),
    url(r'^order/create/$', OrderCreateAPIView.as_view(), name="order-create"),
    url(r'^order/(?P<id>\d+)/edit/$'
        , OrderUpdateAPIView.as_view(), name='order-update'),
    url(r'^order/(?P<id>\d+)/delete/$'
        , OrderDeleteAPIView.as_view(), name='order-delete'),
]
