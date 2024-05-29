import typing
from enum import Enum

from django.db.models import Q
from django.contrib.auth.models import Permission


# All default views: list send-action retrieve update partial_update destroy
class PermissioinType(Enum):
    VIEW = 'view'
    CHANGE = 'change'
    ADD = 'add'
    ACTIONS = 'send_action'


class CheckPermissions:
    user = None

    def __init__(self, user):
        self.user = user

    def _has_perm(self, codename: str):
        if not self.user.is_active:
            return False

        if self.user.is_superuser:
            return True

        has_perm = self.user.user_permissions.filter(codename=codename)
        has_group = self.user.groups.filter(permissions__codename=codename)
        return has_perm.exists() or has_group.exists()

    def has_action_perm(self, viewset, action: str) -> bool:
        codename = f'{self.get_codename(action)}_{viewset.get_view_viewname()}'
        return self._has_perm(codename)

    def has_perm(self, viewset, perm_type: PermissioinType) -> bool:
        codename = f'{perm_type.value}_{viewset.get_view_viewname()}'
        return self._has_perm(codename)

    def has_perm_viewname(self, viewname: str, perm_type: PermissioinType) -> bool:
        codename = f'{perm_type.value}_{viewname}'
        return self._has_perm(codename)

    @classmethod
    def get_codename(cls, action: str) -> str:
        if action in ['list', 'retrieve']:
            return PermissioinType.VIEW.value
        if action in ['update', 'partial_update']:
            return PermissioinType.CHANGE.value
        if action == 'destroy':
            return PermissioinType.DELETE.value
        if action == 'create':
            return PermissioinType.ADD.value

        return action

    @classmethod
    def get_all_permissions(cls, viewset) -> typing.Tuple[str]:
        from custom_admin.api.urls import admin_router as router
        routes = router.get_routes(viewset)

        result = set()
        for route in routes:
            mappings = router.get_method_map(viewset, route.mapping)
            for method, method_name in mappings.items():
                result.add(
                    f'{cls.get_codename(method_name)}_{viewset.get_view_viewname()}'
                )

        return tuple(result)
