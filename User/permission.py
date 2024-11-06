from rest_framework.permissions import IsAuthenticated
from User.models import AdminUser


class AdminRequiredPermission(IsAuthenticated):
    """
    Custom permission to allow only Admins.
    """
    def has_permission(self, request, view):
        return super().has_permission(request, view) and isinstance(request.user, AdminUser)