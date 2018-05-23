from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^menu$', views.ProductListAPIView.as_view(), name='menu'),
    url(r'^order$', views.OrderCreateAPIView.as_view(), name='order-create'),
    url(r'^orders/(?P<customer>\d+)$', views.OrderDetailAPIView.as_view(), name='order-detail'),

    url(r'^order/(?P<id>\d+)/delete$', views.OrderDeleteAPIView.as_view(), name='order-delete'),
    url(r'^order/(?P<id>\d+)/update$', views.OrderUpdateAPIView.as_view(), name='order-update'),
]