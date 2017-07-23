from rest_framework.permissions import BasePermission

from ..models import Order


class IsWaitingOrder(BasePermission):
    message = "This status order changed."

    def has_object_permission(self, request, view, obj):
        order = Order.objects.get(owner=request.user)

        if order.status == "W":
            return True
        return False


class IsOwner(BasePermission):
    message = 'You must be the owner of this object.'

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
