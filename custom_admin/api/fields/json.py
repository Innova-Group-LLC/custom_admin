import typing

from rest_framework import serializers

from .base import AdminBaseFieldMixin


class AdminJsonField(AdminBaseFieldMixin, serializers.JSONField):
    json_forms: typing.Optional[dict]

    def __init__(self, **kwargs):
        self.json_forms = kwargs.pop('json_forms', None)
        super().__init__(**kwargs)
