import datetime

from django.http import HttpResponse
from django.utils.functional import SimpleLazyObject
from django.utils.translation import gettext_lazy as _

from custom_admin.api import fields
from custom_admin.api.action_functions import admin_action
from custom_admin.api.serializers.base_serializer import AdminSerializer

DATETIME_FORMAT = '%Y-%m-%d_%H:%M:%S'


def get_format_choices():
    try:
        from import_export.formats import base_formats
    except ModuleNotFoundError:
        return ()

    return tuple(f.CONTENT_TYPE for f in base_formats.DEFAULT_FORMATS)


class AdminExportSerializer(AdminSerializer):
    method = fields.AdminChoiceField(
        label=_('Export format'), choices=SimpleLazyObject(lambda: get_format_choices()), required=True
    )

    class Meta:
        fields = [
            'method',
        ]


@admin_action(
    short_description=_("Export"),
    icon='mdi-application-export',
    form_serializer=AdminExportSerializer,
    base_color='#6699ff',
    variant='outlined',
)
def admin_export(view, request, queryset, form_data, *args, **kwargs):
    assert view.resource, f'{view.__class__.__name__}.resource is required'
    resource = view.resource

    serializer = AdminExportSerializer(data=form_data)
    serializer.is_valid(raise_exception=True)
    method = serializer.validated_data['method']

    file_format = None
    from import_export.formats import base_formats
    for f in base_formats.DEFAULT_FORMATS:
        if f.CONTENT_TYPE == method:
            file_format = f

    if not file_format:
        raise Exception('"{method}" export format is not found')

    file_format = file_format(encoding='utf-8-sig')

    dataset = resource().export(queryset)
    export_data = file_format.export_data(dataset=dataset)

    content_type = file_format.get_content_type()
    response = HttpResponse(export_data, content_type=content_type)

    time = datetime.datetime.now().strftime(DATETIME_FORMAT)
    filename = f'{view.get_view_viewname()}_{time}.{file_format.get_extension()}'
    response["Content-Disposition"] = 'attachment; filename="%s"' % (filename,)
    response['Pragma'] = filename

    from import_export.signals import post_export
    post_export.send(sender=None, model=queryset.model)
    return response
