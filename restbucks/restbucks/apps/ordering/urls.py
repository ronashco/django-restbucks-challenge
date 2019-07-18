from django.urls import path

from .views import OrderingMenuAPIView, OrderingAPIView, OrderingDeleteUpdateAPIView


urlpatterns = [
    path('menu/', OrderingMenuAPIView.as_view(), name='ordering-menu'),
    path(
        '<int:pk>/',
        OrderingDeleteUpdateAPIView.as_view(),
        name='ordering-delete-or-change'
    ),
    path('', OrderingAPIView.as_view(), name='ordering-orders'),
]
