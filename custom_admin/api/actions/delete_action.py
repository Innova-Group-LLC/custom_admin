import typing

from django.db.models.deletion import ProtectedError
from django.utils.translation import gettext as _


def delete_action(view, request, queryset, *args, **kwargs):
    try:
        queryset.delete()
    except ProtectedError as e:
        return _(
            'Невозможно удалить некоторые экземпляры модели, '
            'поскольку на них ссылаются через защищенные внешние ключи: %(objects)s') % {
                   'objects': ", ".join([str(obj) for obj in e.protected_objects])
               }, 400

    return _('Записи успешно удалены!'), 200


delete_action.short_description = _("Удалить")
