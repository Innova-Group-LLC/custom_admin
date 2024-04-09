from rest_framework import serializers
from django.utils.translation import gettext as _


class AdminChoiceField(serializers.ChoiceField):
    def __init__(self, *args, **kwargs):
        kwargs.pop("child", None)
        self.max_width = kwargs.pop("max_width", None)
        super().__init__(*args, **kwargs)

    def to_representation(self, value):
        if isinstance(value, list):
            return value

        if value in self._choices:
            return {"value": value, "text": self._translate_value(self._choices[value])}

        return {"value": value, "text": self._translate_value(value)}

    def _translate_value(self, value):
        if isinstance(value, int):
            return value
        return str(_(value))

    def to_internal_value(self, data):
        if data == '' and self.allow_blank:
            return ''

        value = data
        if isinstance(data, dict):
            value = data["value"]

        for key, val in self._choices.items():
            if key == value:
                return value

        self.fail('invalid_choice', input=data)
