import datetime
import typing
from io import BytesIO

from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _

from custom_admin.api.action_functions import admin_action


def get_list_display(view):
    list_display = getattr(view, 'list_display', None)
    if list_display:
        return list_display

    meta = view.metadata_class()
    serializer_class = view().get_serializer_class()
    serializer_info = meta.get_serializer_info(serializer_class())
    return serializer_info.keys()


def _get_headers(view, serializer, serializer_class):
    meta = view.metadata_class()
    serializer_info = meta.get_serializer_info(serializer_class())
    field_data = {
        field: data.get('label')
        for field, data in serializer_info.items()
    }
    serializer_fields = getattr(serializer, 'get_fields', {})
    headers = []
    for column in get_list_display(view):
        serializer_field = serializer_fields.get(column)
        if serializer_field and serializer_field.label:
            headers.append(serializer_field.label)
        elif column in field_data:
            headers.append(field_data[column])
        else:
            headers.append(column)

    return headers


def base_export_csv(filename: str, columns: typing.List, lines: typing.List):
    f = BytesIO()
    import unicodecsv as csv
    writer = csv.writer(f, dialect=csv.excel, encoding='utf-8')
    writer.writerow(columns)

    for line in lines:
        writer.writerow(line)
    f.seek(0)

    response = HttpResponse(f, content_type='text/csv')
    response['Pragma'] = filename
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    f.close()
    return response


@admin_action(
    short_description=_("Выгрузить в csv"),
    icon='mdi-application-export',
)
def export_csv_action(view, request, queryset, *args, **kwargs):
    'Depricated'

    serializer_class = view().get_serializer_class()
    serializer = serializer_class(queryset, many=True, context={'request': request})

    columns = _get_headers(view, serializer, serializer_class)
    filename = f'{view.get_view_viewname()}_{datetime.datetime.now()}.csv'

    lines = []
    for data in serializer.data:
        line_data = []

        for column in get_list_display(view):
            value = data.get(column, None)
            if isinstance(value, dict):
                value = value.get('text', value)

            line_data.append(value)

        lines.append(line_data)

    return base_export_csv(filename, columns, lines)
