import typing
from dataclasses import dataclass

from django.utils.module_loading import import_string


@dataclass
class AdminViewSetInfo:
    group_slug: str
    title: str

    views: typing.List[str]

    # https://element.eleme.io/#/en-US/component/icon
    icon: typing.Optional[str] = None

    def __post_init__(self):
        assert len(self.views) > 0, 'AdminViewSetInfo.views is empty'

    def iterate_views(self):
        from custom_admin.api.views import BaseAdminDataViewSet, BaseAdminViewSet

        for view_class_path in self.views:
            view = import_string(view_class_path)
            assert issubclass(view, (BaseAdminDataViewSet, BaseAdminViewSet)), f'Admin viewset "{view_class_path}" {view.__name__} must be instance of BaseAdminDataViewSet or BaseAdminViewSet'
            yield view

    def asdict(self):
        return {
            'group': self.group_slug,
            'group_title': self.title,
            'group_icon': self.icon,
        }
