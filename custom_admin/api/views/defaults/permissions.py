from django.contrib.auth.models import Permission
from custom_admin.api.views.base_admin_viewset import BaseAdminViewSet
from django.utils.translation import gettext_lazy as _


class PermissionsAdminViewSet(BaseAdminViewSet):
    title = _('Права доступа')
    queryset = Permission.objects.all().select_related('content_type')
    search_fields = ['id', 'name', 'codename']
    filterset_fields = ['content_type']
    list_display = (
        'id',
        'name',
        'codename',
        'content_type',
    )
