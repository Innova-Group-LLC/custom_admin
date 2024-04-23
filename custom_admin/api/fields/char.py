import typing

from rest_framework import serializers

from .base import AdminBaseFieldMixin


class AdminCharField(AdminBaseFieldMixin, serializers.CharField):
    '''
    Поле wysiwyg используется на фронте для отображения
    визуального редактора текста. Он сохраняет текст в формате html.

    multilined - для отображения текстового поля в несколько строк
    '''

    wysiwyg: bool
    multilined: bool
    tag_style: typing.Optional[dict]

    def __init__(self, **kwargs):
        self.wysiwyg = kwargs.pop('wysiwyg', False)
        self.tag_style = kwargs.pop('tag_style', {})
        self.multilined = kwargs.pop('multilined', False)
        super().__init__(**kwargs)
