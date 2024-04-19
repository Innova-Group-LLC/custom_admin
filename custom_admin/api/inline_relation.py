import typing
from dataclasses import asdict, dataclass

from rest_framework import serializers

INLINE_VIEWSET_NAME_ERROR = '''
View {class_name}.related_inlines[{i}].viewset_name not existed.

Plsease, check manage.py custom_admin_viewsets_list'''

INLINE_VIEWSET_NOT_ORM = '''
View {class_name}.related_inlines[{i}].viewset_name error:

Viewset {target_viewset} don't have get_model.
Are you sure its ORM viewset?'''


@dataclass
class RelatedInline:
    title: str

    # manage.py custom-admin-viewsets-list
    viewset_name: str

    inline_slug: str

    # In case of ORM related viewset
    back_relation_name: typing.Optional[str] = None

    # https://element.eleme.io/#/en-US/component/icon
    icon: typing.Optional[str] = None

    def asdict(self) -> dict:
        return asdict(self)

    def validate(self, viewset, index):
        from custom_admin.utils.register_admin_viewsets import _ADMIN_VIEWS
        target_viewset = _ADMIN_VIEWS[self.viewset_name]
        if not target_viewset:
            raise serializers.ValidationError(INLINE_VIEWSET_NAME_ERROR.format(class_name=viewset.__name__, i=index))

        if self.back_relation_name:
            if not hasattr(target_viewset, 'get_model'):
                raise serializers.ValidationError(INLINE_VIEWSET_NOT_ORM.format(
                    class_name=viewset.__name__,
                    i=index,
                    target_viewset=target_viewset.__name__,
                ))
