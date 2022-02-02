"""Rouser for shipment application"""
from rest_framework import routers
from orders.views import (OrderAPIView, )

router = routers.SimpleRouter()
router.register(r'actions', OrderAPIView, "order_actions")

urlpatterns = [
            ]

urlpatterns += router.urls
