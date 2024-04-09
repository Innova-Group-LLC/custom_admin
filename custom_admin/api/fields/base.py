from rest_framework import serializers


class AdminBaseFieldMixin:
    update_only = None
    create_only = None
    list_only = None

    def __init__(self, **kwargs):
        self.update_only = kwargs.pop('update_only', False)
        self.create_only = kwargs.pop('create_only', False)
        self.list_only = kwargs.pop('list_only', False)
        super().__init__(**kwargs)
