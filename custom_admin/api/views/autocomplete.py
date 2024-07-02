# pylint: disable=W0201
import logging
import operator
import typing
from dataclasses import dataclass
from functools import reduce

from django.apps import apps
from django.db import models
from django.db.models import Manager, Q
from django.db.models.query import QuerySet
from django_filters.utils import get_model_field
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from custom_admin.api.permissions import AdminPermission

log = logging.getLogger("admin")

INT_FIELDS = (
    models.PositiveIntegerField,
    models.IntegerField,
    models.AutoField,
    models.BigIntegerField,
)


@dataclass
class AutocompleteInfo:
    viewname: str
    field_slug: str
    is_filter: bool
    form_data: typing.Optional[dict]
    action_name: typing.Optional[str]


class AnyField(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        return data


class AutoCompeteSerializer(serializers.Serializer):
    viewname = serializers.CharField(required=False)
    is_filter = serializers.BooleanField(default=False)
    action_name = serializers.CharField(required=False)
    field_slug = serializers.CharField(required=False)

    form_data = serializers.JSONField(required=False)

    search_string = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    limit = serializers.IntegerField(required=False, allow_null=True)
    existed_choices = serializers.ListField(
        child=AnyField(),
        required=False,
        allow_empty=True,
        allow_null=True,
    )


class AutoCompeteView(APIView):
    throttle_classes = []
    permission_classes = (AdminPermission,)

    default_fields = {
        'Permission': ('id', 'codename', 'name'),
        'Group': ('id', 'name'),
        'Country': ('id', 'name', 'alt_names__name'),
        'City': ('id', 'name', 'alt_names__name'),
        'ContentType': ('id', 'model', 'app_label')
    }

    def get_search_filter(self, model, search_string: str):
        filters = []

        autocomplite_fields = getattr(
            model, 'admin_autocomplite_fields',
            self.default_fields.get(model.__name__, ('pk',))
        )

        for field_name in autocomplite_fields:
            field = get_model_field(model, field_name)
            value = search_string

            filter_lookup = None
            if issubclass(field.__class__, INT_FIELDS):
                # Int field
                try:
                    value = int(search_string)
                    filter_lookup = f'{field_name}__exact'
                except ValueError:
                    continue
            else:
                # String field
                filter_lookup = f'{field_name}__icontains'

            if filter_lookup:
                field_filter = Q(**{filter_lookup: value})
                filters.append(field_filter)

        if not filters:
            return None

        return reduce(operator.or_, filters)

    def get_queryset_by_view(self, model, request):

        if self.action_name or self.is_filter:
            return model.objects.all()

        if self.viewname:
            from custom_admin.utils.register_admin_viewsets import _ADMIN_VIEWS
            view = _ADMIN_VIEWS[self.viewname]
            serializer = view().get_serializer_class()()

            field = serializer.fields.get(self.field_slug)
            if not field:
                raise serializers.ValidationError(
                    f'Model {self.app_label}.{self.model_name} view "{self.viewname}" field slug "{self.field_slug}" is not found'
                )

            if isinstance(field, serializers.ManyRelatedField):
                field = field.child_relation

            filter_queryset = getattr(field, 'filter_queryset', None)
            qs = getattr(field, 'queryset')

            if filter_queryset:
                filtered_qs = filter_queryset(qs, self.form_data, self.request)
                log.debug(
                    'AUTOCOMPLETE view:%s using:%s init form_data.keys:%s result:%s',
                    self.viewname, filter_queryset.__name__, self.form_data.keys(), filtered_qs,
                )
                return filtered_qs

            if not isinstance(qs, (QuerySet, Manager)):
                raise serializers.ValidationError(f'Model {self.app_label}.{self.model_name} view "{self.viewname}" autocomplete for {self.field_slug}')

            return qs.all()

        else:
            raise NotImplementedError('')

    @staticmethod
    def _get_str_value(obj):
        if not obj:
            return

        try:
            return str(obj) or str(obj.id)
        except TypeError as e:
            log.error('Admin autocomplete: error get __str__ for %s', obj)
            return str(obj.id)

    def post(self, request, model_name, app_label, *args, **kwargs):
        self.app_label = app_label
        self.model_name = model_name

        self.serializer = AutoCompeteSerializer(data=request.data)
        self.serializer.is_valid(raise_exception=True)

        model = apps.get_model(app_label=app_label, model_name=model_name)
        if not model:
            raise serializers.ValidationError(f'Model {self.app_label}.{self.model_name} not found')

        self.viewname = self.serializer.validated_data.get('viewname')
        self.form_data = self.serializer.validated_data.get('form_data', {})
        self.field_slug = self.serializer.validated_data.get('field_slug')
        self.action_name = self.serializer.validated_data.get('action_name')
        self.is_filter = self.serializer.validated_data.get('is_filter')

        view_queryset = self.get_queryset_by_view(model, request)
        qs = view_queryset

        autocomplete_filter = getattr(qs.model, 'autocomplete_filter', None)
        if callable(autocomplete_filter):
            qs = autocomplete_filter(
                request,
                qs,
                AutocompleteInfo(
                    viewname=self.viewname,
                    action_name=self.action_name,
                    is_filter=self.is_filter,

                    field_slug=self.field_slug,
                    form_data=self.form_data,
                )
            )

        search_string = self.serializer.validated_data.get('search_string')
        if search_string:
            filters = self.get_search_filter(model, search_string)
            if not filters:
                return Response([])
            qs = qs.filter(filters).order_by('pk').distinct('pk')

        limit = self.serializer.validated_data.get('limit')
        if limit:
            qs = qs[:limit]

        existed_choices = self.serializer.validated_data.get('existed_choices', [])
        if existed_choices:

            # Добавляет в результат уже выбранные варианты
            filter_ids = view_queryset.filter(pk__in=existed_choices)
            if qs:
                qs = qs.union(filter_ids)
            else:
                qs = filter_ids

        formated_values = [
            {'id': obj.pk, 'text': self._get_str_value(obj)}
            for obj in qs
        ]
        return Response(formated_values)
