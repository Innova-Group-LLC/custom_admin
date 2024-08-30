from django.db.models.deletion import ProtectedError
from django.utils.translation import gettext as _

from custom_admin.api.action_functions import admin_action

RELATED_ERROR = _('It is not possible to delete some model instances because they are referenced via protected foreign keys: %(objects)s')

@admin_action(
    short_description=_("Delete"),
    icon='mdi-delete-forever',
    base_color='#ff3333',
    variant='outlined',
    confirmation_text=_('Are you sure you want to delete the selected records?'),
)
def delete_action(view, request, queryset, *args, **kwargs):
    try:
        # Get rid of distinct in case of "Cannot call delete() after .distinct()"
        if queryset.query.distinct or queryset.query.distinct_fields:
            queryset = queryset.model.objects.filter(pk__in=queryset.values_list('pk'))

        queryset.delete()
    except ProtectedError as e:
        return RELATED_ERROR % {'objects': ", ".join([str(obj) for obj in e.protected_objects])}, 400

    return _('Records have been successfully deleted!'), 200
