from collections import OrderedDict

from django.db import models
from django_filters import filters, filterset
from django_filters import rest_framework as drf_filters
from rest_framework import fields as drf_fields

from custom_admin.api.filters.date_range import AdminDateFromToRangeFilter


class AdminFilterSetMetaclass(filterset.FilterSetMetaclass):
    @classmethod
    def get_declared_filters(cls, bases, attrs):
        new_filters = [
            (filter_name, attrs.pop(filter_name))
            for filter_name, obj in list(attrs.items())
            if isinstance(obj, (filters.Filter, drf_fields.Field))
        ]

        for filter_name, f in new_filters:
            if hasattr(f, 'field_name') and getattr(f, 'field_name', None) is None:
                f.field_name = filter_name

        known = set(attrs)

        def visit(name):
            known.add(name)
            return name

        base_filters = [
            (visit(name), f)
            for base in bases if hasattr(base, 'declared_filters')
            for name, f in base.declared_filters.items() if name not in known
        ]

        return OrderedDict(base_filters + new_filters)


class BaseAdminFilterSet(drf_filters.FilterSet, metaclass=AdminFilterSetMetaclass):
    FILTER_DEFAULTS = drf_filters.FilterSet.FILTER_DEFAULTS
    FILTER_DEFAULTS[models.ForeignKey] = {
        'filter_class': filters.ModelMultipleChoiceFilter,
        'extra': lambda f: {
            'queryset': filterset.remote_queryset(f),
        }
    }
    FILTER_DEFAULTS[models.DateTimeField] = {
        'filter_class': AdminDateFromToRangeFilter,
    }
