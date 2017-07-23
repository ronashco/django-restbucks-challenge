from django.conf.urls import include, url
from views import OrderCreateAPIView, OrderListAPIView


urlpatterns = [
    url(r'^$', OrderListAPIView.as_view(), name="order"),
    url(r'^order/$', OrderListAPIView.as_view(), name="order"),
    url(r'^order/create/$', OrderCreateAPIView.as_view(), name="order-create")
]
