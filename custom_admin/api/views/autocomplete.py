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


class ModelNotFound(Exception):
    pass


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

    def get_model(self, request):
        app_label = request.data.get('app_label')
        if not app_label:
            raise ModelNotFound('app_label is required field')

        model_name = request.data.get('model_name')
        if not model_name:
            raise ModelNotFound('model_name is required field')

        model = apps.get_model(app_label=app_label, model_name=model_name)
        if not model:
            raise ModelNotFound(f'Model {app_label}.{model_name} not found')

        return model

    def get_queryset_by_view(self, model, request):
        viewname = request.data.get('viewname')
        if viewname:
            from custom_admin.utils.register_admin_viewsets import _ADMIN_VIEWS
            view = _ADMIN_VIEWS[viewname]
            serializer = view.get_serializer_class()()

            field_slug = request.data.get('field_slug')
            field = serializer.fields.get(field_slug)

            if field:

                if isinstance(field, serializers.ManyRelatedField):
                    field = field.child_relation

                filter_queryset = getattr(field, 'filter_queryset', None)
                qs = getattr(field, 'queryset')

                form_data = request.data.get('form_data')
                if form_data is None:
                    form_data = dict()

                if filter_queryset:
                    filtered_qs = filter_queryset(qs, form_data, request)
                    log.debug(
                        'AUTOCOMPLETE view:%s using:%s init form_data.keys:%s result:%s',
                        viewname, filter_queryset.__name__, form_data.keys(), filtered_qs,
                    )
                    return filtered_qs

                if qs and isinstance(qs, (QuerySet, Manager)):
                    return qs.all()
        return model.objects.all()

    @staticmethod
    def _get_str_value(obj):
        if obj:
            try:
                return str(obj) or str(obj.id)
            except TypeError as e:
                log.error('Admin autocomplete: error get __str__ for %s', obj)
                return str(obj.id)

    def post(self, request, format=None):
        search_string = request.data.get('search_string')
        limit = request.data.get('limit')

        try:
            model = self.get_model(request)
        except ModelNotFound as e:
            return Response(str(e))

        view_queryset = self.get_queryset_by_view(model, request)
        qs = view_queryset
        if search_string:
            filters = self.get_search_filter(model, search_string)
            if not filters:
                return Response([])
            qs = qs.filter(filters).order_by('id').distinct('id')

        if limit:
            qs = qs[:limit]

        existed_choices = request.data.get('existed_choices', [])
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
