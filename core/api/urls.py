from django.conf.urls import url
from . import views

"""
All of the following urls have 'api/' prefix by default.
"""

urlpatterns = [
    url(r'^products/$', views.Menu.as_view(), name='menu'),
    url(r'^accounts/register/$', views.register, name='register'),
    url(r'^accounts/login/$', views.login, name='login'),
    url(r'^cart/$', views.OrdersListView.as_view(), name='cart-list')
]
