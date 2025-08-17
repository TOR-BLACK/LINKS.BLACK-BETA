from rest_framework import permissions

from apps.users.utils import UserRole


class AdminPanelCustomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        '''user = request.user
        if user.role == UserRole.OWNER:
            return True
        required_roles = getattr(view, 'permission_required_roles', list())
        return user.role in required_roles'''
        return True
