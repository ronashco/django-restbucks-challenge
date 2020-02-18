from django.urls import path

from coffeeshop.views import ProductListView, CreateOrderView, UserOrdersView, CancelOrderView, EditOrderView
from . import views

urlpatterns = [
    # path("", views.index, name="index"),
    path('menu', ProductListView.as_view(), name='product_list'),
    path('order', CreateOrderView.as_view(), name='order_create'),
    path('order/list', UserOrdersView.as_view(), name='order_list'),
    path('order/cancel', CancelOrderView.as_view(), name='order_cancel'),
    path('order/edit', EditOrderView.as_view(), name='order_edit'),
]
