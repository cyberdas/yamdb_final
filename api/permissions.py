from rest_framework import permissions

from users.models import UserRole

class IsAdminUserOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or request.user.is_superuser

class IsAdminOrAuthor(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user == obj.author or request.user.role in (UserRole.admin, UserRole.moderator)

class IsAdminOrProhibited(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_superuser or request.user.role == UserRole.admin
