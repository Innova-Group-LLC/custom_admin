import datetime

from django.utils.translation import gettext_lazy as _

from custom_admin.api.actions.export_csv_action import base_export_csv
from custom_admin.api.inlines.inline_table import InlineTableResult


def export_csv_inline(view, request, result: InlineTableResult, *args, **kwargs):
    data = result.asdict()
    columns = data.get('columns')
    lines = data.get('data')
    filename = f'{view.__name__}_{datetime.datetime.now()}.csv'
    return base_export_csv(filename, columns, lines)


export_csv_inline.short_description = _("Выгрузить в csv (кодировка UTF-8)")
