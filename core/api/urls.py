from django.conf.urls import url
from . import views

"""
All of the following urls have 'api/' prefix by default.
"""

urlpatterns = [
    url(r'^products/$', views.Menu.as_view(), name='menu'),
    url(r'^accounts/register/$', views.register, name='register'),
    url(r'^accounts/login/$', views.login, name='login'),
    url(r'^orders/$', views.OrderListCreateView.as_view(), name='orders'),
    url(r'^orders/(?P<order_id>[\d]+)/$', views.OrderView.as_view(), name='order'),
    url(r'^orders/(?P<order_id>[\d]+)/product/(?P<product_id>[\d]+)/$',
        views.OrderProductView.as_view(),
        name='order-product'),
    url(r'^orders/cart/$', views.CartView.as_view(), name='cart'),
]
