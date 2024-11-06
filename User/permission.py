from rest_framework.permissions import IsAuthenticated
from User.models import AdminUser


class AdminRequiredPermission(IsAuthenticated):
    """
    Custom permission to allow only Admins.
    """
    def has_permission(self, request, view):
            # Ensure the user is authenticated and is an instance of AdminUser
            is_authenticated = super().has_permission(request, view)

            # Try retrieving the AdminUser instance
            try:
                admin_user = AdminUser.objects.get(pk=request.user.pk)
                is_admin = admin_user is not None
            except AdminUser.DoesNotExist:
                is_admin = False

            return is_authenticated and is_admin