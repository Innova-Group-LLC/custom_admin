from rest_framework import serializers

from .base import AdminBaseFieldMixin


class AdminIntField(AdminBaseFieldMixin, serializers.IntegerField):
    pass
