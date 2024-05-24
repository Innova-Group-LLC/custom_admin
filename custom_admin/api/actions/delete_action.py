from django.db.models.deletion import ProtectedError
from django.utils.translation import gettext as _

from custom_admin.api.action_functions import admin_action


@admin_action(
    short_description=_("Удалить"),
    icon='mdi-delete-forever',
    base_color='red',
    confirmation_text=_('Вы уверены, что хотите удалить выбранные записи?'),
)
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
