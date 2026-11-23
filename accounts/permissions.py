from rest_framework.permissions import BasePermission


class IsAdminRole(BasePermission):
    """Allows access only to users with role=ADMIN (or Django superusers)."""

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and (user.is_admin or user.is_superuser))


class IsOwnerOrAdmin(BasePermission):
    """Object-level: owner of the object, or an admin, may access it."""

    def has_object_permission(self, request, view, obj):
        user = request.user
        owner = getattr(obj, "owner", None) or getattr(obj, "customer", None)
        return bool(user.is_admin or user.is_superuser or owner == user)
