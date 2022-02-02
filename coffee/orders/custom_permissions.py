"""Custom permissions classes"""
from rest_framework import permissions

class CustomPermissions(permissions.BasePermission):
    """Check if user catch his own info"""
    def has_object_permission(self, request, view, obj):
        """Return permissions for user to catch his own object"""
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_staff

    def has_permission(self, request, view):
        return request.user.is_authenticated
