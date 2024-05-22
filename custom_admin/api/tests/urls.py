import typing

from django.urls import include, path

from custom_admin.api.viewset_info import AdminViewSetInfo

ADMIN_URLS: typing.List[AdminViewSetInfo] = [
    AdminViewSetInfo(
        group_slug='test',
        title='test',
        views=[
            'custom_admin.api.views.defaults.GroupAdminViewSet',
            'custom_admin.api.views.defaults.PermissionsAdminViewSet',
            'custom_admin.api.views.defaults.AdminLogAdminViewSet',
        ]
    ),
]

urlpatterns = [
    path('custom_admin/', include('custom_admin.api.urls')),
]
