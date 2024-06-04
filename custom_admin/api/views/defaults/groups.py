from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from custom_admin.api.views.base_admin_viewset import BaseAdminViewSet


class GroupAdminViewSet(BaseAdminViewSet):
    queryset = Group.objects.all()
    search_fields = ('name', )
    list_display = (
        'id',
        'name',
    )
