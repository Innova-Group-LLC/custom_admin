import logging
import operator
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


class AutoCompeteSerializer(serializers.Serializer):
    viewname = serializers.CharField(required=False)
    field_slug = serializers.JSONField(required=False)

    search_string = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    limit = serializers.IntegerField(required=False, allow_null=True)
    existed_choices = serializers.ListField(
        child=serializers.IntegerField(),
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
            self.default_fields.get(model.__name__, ('id',))
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

    def get_queryset_by_view(self, model, viewname, form_data, field_slug):

        if not viewname:
            return model.objects.all()

        from custom_admin.utils.register_admin_viewsets import _ADMIN_VIEWS
        view = _ADMIN_VIEWS[viewname]
        serializer = view.get_serializer_class()()

        field = serializer.fields.get(field_slug)

        if field:

            if isinstance(field, serializers.ManyRelatedField):
                field = field.child_relation

            filter_queryset = getattr(field, 'filter_queryset', None)
            qs = getattr(field, 'queryset')

            if form_data is None:
                form_data = {}

            if filter_queryset:
                filtered_qs = filter_queryset(qs, form_data, self.request)
                log.debug(
                    'AUTOCOMPLETE view:%s using:%s init form_data.keys:%s result:%s',
                    viewname, filter_queryset.__name__, form_data.keys(), filtered_qs,
                )
                return filtered_qs

            if qs and isinstance(qs, (QuerySet, Manager)):
                return qs.all()

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
        serializer = AutoCompeteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        search_string = serializer.validated_data.get('search_string')
        limit = serializer.validated_data.get('limit')

        model = apps.get_model(app_label=app_label, model_name=model_name)
        if not model:
            raise serializers.ValidationError(f'Model {app_label}.{model_name} not found')

        view_queryset = self.get_queryset_by_view(
            model,
            viewname=serializer.validated_data.get('viewname'),
            form_data=serializer.validated_data.get('form_data'),
            field_slug=serializer.validated_data.get('field_slug'),
        )

        qs = view_queryset
        if search_string:
            filters = self.get_search_filter(model, search_string)
            if not filters:
                return Response([])
            qs = qs.filter(filters).order_by('id').distinct('id')

        if limit:
            qs = qs[:limit]

        existed_choices = serializer.validated_data.get('existed_choices', [])
        if existed_choices:

            # Добавляет в результат уже выбранные варианты
            filter_ids = view_queryset.filter(id__in=existed_choices)
            if qs:
                qs = qs.union(filter_ids)
            else:
                qs = filter_ids

        formated_values = [
            {'id': obj.id, 'text': self._get_str_value(obj)}
            for obj in qs
        ]
        return Response(formated_values)
