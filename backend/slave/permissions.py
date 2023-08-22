from rest_framework.permissions import BasePermission


class IsSlaveAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return request.slave is not None
