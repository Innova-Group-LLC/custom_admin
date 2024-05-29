import logging

from custom_admin.controllers.permissions import CheckPermissions, PermissioinType
from rest_framework.permissions import BasePermission

logger = logging.getLogger('custom_admin')


class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user.is_staff or not user.is_active:
            logger.info(
                'ADMIN BYPASS User #%s username:%s is_staff:%s is_active:%s',
                user.id, user.username, user.is_staff, user.is_active,
            )
            return False

        return True


class AdminViewsPermission(BasePermission):
    def has_permission(self, request, view):
        return CheckPermissions(request.user).has_view_perm(view)
