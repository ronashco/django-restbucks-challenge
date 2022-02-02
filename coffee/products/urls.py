"""Rouser for shipment application"""
from rest_framework import routers
from products.views import (ProductsAPIView, )

router = routers.SimpleRouter()
router.register(r'actions', ProductsAPIView, "product_actions")

urlpatterns = [
            ]

urlpatterns += router.urls
