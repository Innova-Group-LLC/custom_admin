import logging

from django.contrib.contenttypes.models import ContentType
from rest_framework.permissions import BasePermission

logger = logging.getLogger('custom_admin')


class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user.is_staff and not user.is_superuser:
            logger.info('ADMIN BYPASS User #%s: User is not saff or superuser', user.id)
            return False

        if not user.is_superuser and view and hasattr(view, 'get_model'):
            model = view.get_model()
            if model is not None:
                content_type = ContentType.objects.get_for_model(model)
                has_perm = user.user_permissions.filter(
                    content_type=content_type
                ).exists()
                if not has_perm:
                    return False

        return True
