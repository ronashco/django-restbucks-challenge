from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^panel', views.panel, name='panel'),
    url(r'^menu', views.menu, name='menu'),
    url(r'^logout', views.signout, name='logout'),
    url(r'^orders', views.view_orders, name='orders'),
    url(r'^order', views.new_order, name='order'),
    url(r'^change_order', views.change_order, name='change_order'),
    url(r'^cancel_order', views.cancel_order, name='cancel_order'),
    url(r'^view_an_order', views.view_an_order, name='view_an_order'),
]
