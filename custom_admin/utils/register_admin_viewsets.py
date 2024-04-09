from django.conf import settings
from rest_framework import routers

from custom_admin.api.viewset_info import AdminViewSetInfo

_ADMIN_VIEWS = {}


def register_admin_viewsets(admin_router: routers.SimpleRouter):
    group: AdminViewSetInfo
    for group in settings.ADMIN_URLS:

        for view in group.iterate_views():
            viewname = view.get_view_viewname()

            _ADMIN_VIEWS[viewname] = view
            view._info = group

            admin_router.register(
                prefix=viewname,
                viewset=view,
                basename=viewname
            )
