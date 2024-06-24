from enum import Enum

from django.utils.translation import gettext as _


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
    def get_title(cls, action: str) -> str:
        if action in ['list', 'retrieve']:
            return _('View')
        if action in ['update', 'partial_update']:
            return _('Change')
        if action == 'destroy':
            return _('Destroy')
        if action == 'create':
            return _('Create')
        if action == 'send_action':
            return _('Send action')

        return _(action)

    @classmethod
    def get_all_permissions(cls, viewset) -> dict:
        from custom_admin.api.urls import admin_router as router
        routes = router.get_routes(viewset)

        result = {}
        for route in routes:
            mappings = router.get_method_map(viewset, route.mapping)
            for _method, method_name in mappings.items():
                slug = cls.get_codename(method_name)
                codename = f'{slug}_{viewset.get_view_viewname()}'
                result[codename] = {
                    'slug': slug,
                    'viewname': viewset.get_view_viewname(),
                    'title': f'{cls.get_title(method_name)} | {viewset.get_view_title()}',
                }

        return result
