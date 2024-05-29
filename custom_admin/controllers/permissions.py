import typing
from enum import Enum

from django.db.models import Q


# All default views: list send-action retrieve update partial_update destroy
class PermissioinType(Enum):
    VIEW = 'view'
    CHANGE = 'change'
    ADD = 'add'
    DELETE = 'delete'


class CheckPermissions:
    user = None

    def __init__(self, user):
        self.user = user

    def _has_perm(self, codename: str):
        if not self.user.is_active:
            return False

        if self.user.is_superuser:
            return True

        return self.user.filter(
            Q(groups__codename=codename) |
            Q(user_permissions__codename=codename)
        ).exists()

    def has_view_perm(self, viewset) -> bool:
        print('viewset.action_map', viewset.action_map)
        raise Exception(viewset.action_map)
        method = request.method.lower()
        action = viewset.action_map.get(method)

        codename = f'{self.get_codename(action)}_{viewset.get_view_viewname()}'
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
            for method, slug in mappings.items():
                result.add(
                    f'{cls.get_codename(slug)}_{viewset.get_view_viewname()}'
                )

        return tuple(result)
