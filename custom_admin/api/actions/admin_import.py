from io import TextIOWrapper

from django.utils.translation import gettext_lazy as _

from custom_admin.api import fields
from custom_admin.api.action_functions import admin_action
from custom_admin.api.actions.admin_export import AdminExportSerializer


class AdminImportSerializer(AdminExportSerializer):
    file = fields.Base64FileField(
        label=_('File'), required=True
    )

    class Meta(AdminExportSerializer.Meta):
        fields = AdminExportSerializer.Meta.fields + [
            'file',
        ]


@admin_action(
    short_description=_("Import"),
    icon='mdi-application-import',
    form_serializer=AdminImportSerializer,
    allow_empty_selection=True,
    base_color='#6699ff',
    variant='outlined',
)
def admin_import(view, request, queryset, form_data, *args, **kwargs):
    assert view.resource, f'{view.__class__.__name__}.resource is required'
    resource = view.resource()

    serializer = AdminImportSerializer(data=form_data)
    serializer.is_valid(raise_exception=True)
    method = serializer.validated_data['method']
    file = serializer.validated_data['file']

    file_format = None
    from import_export.formats import base_formats
    for f in base_formats.DEFAULT_FORMATS:
        if f.CONTENT_TYPE == method:
            file_format = f

    file_format = file_format()

    f = TextIOWrapper(file, encoding='ascii', errors='replace')
    dataset = file_format.create_dataset(f)
    result = resource.import_data(
        dataset,
        dry_run=False,
        use_transactions=False,
        collect_failed_rows=True,
        rollback_on_validation_errors=False,
    )

    if result.has_errors():
        errors = '</br>'.join(str(e) for e in result.row_errors())
        return _('Import errors: %s</br>%s') % (result.base_errors, errors,), 400

    ids = ", ".join(tuple(str(i.object_id) for i in result.valid_rows()))
    return _('Successfully created/updated records: %s') % (ids,), 200
