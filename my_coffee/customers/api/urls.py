from django.conf.urls import url
from views import OrderCreateAPIView, OrderListAPIView\
    , OrderUpdateAPIView, OrderDeleteAPIView, UserLoginAPIView\
    , UserCreateAPIView


urlpatterns = [
    url(r'^$', OrderListAPIView.as_view(), name="order"),
    url(r'^order/$', OrderListAPIView.as_view(), name="order"),
    url(r'^order/create/$', OrderCreateAPIView.as_view(), name="order-create"),
    url(r'^order/(?P<id>\d+)/edit/$'
        , OrderUpdateAPIView.as_view(), name='order-update'),
    url(r'^order/(?P<id>\d+)/delete/$'
        , OrderDeleteAPIView.as_view(), name='order-delete'),
    url(r'^login/$', UserLoginAPIView.as_view(), name='login'),
    url(r'^register/$', UserCreateAPIView.as_view(), name='register'),
]
