from datetime import datetime, time

from django_filters import filters
from django_filters.fields import forms

FORMAT = '%Y-%m-%dT%H:%M:%S'


class AsIsField(forms.Field):
    def to_python(self, value):
        return value


class AdminDateFromToRangeFilter(filters.DateFromToRangeFilter):
    field_class = AsIsField

    def filter(self, qs, value):
        if value:
            _from = datetime.combine(datetime.strptime(value['from'], FORMAT), time.min)
            to = datetime.combine(datetime.strptime(value['to'], FORMAT), time.max)
            return qs.filter(**{
                f'{self.field_name}__gte': _from,
                f'{self.field_name}__lte': to,
            })
        return super().filter(qs, value)
