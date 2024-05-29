import json
import typing
from json.decoder import JSONDecodeError
from urllib.parse import unquote

from django_filters import rest_framework
from rest_framework import filters, serializers

from custom_admin.api.filters.base_admin_filter import BaseAdminFilterSet


def get_filter_info(request) -> typing.Optional[dict]:
    if not request.GET or 'filter_info' not in request.GET:
        return

    filter_info = request.GET['filter_info']
    if not filter_info:
        return

    try:
        return json.loads(unquote(filter_info))
    except JSONDecodeError as e:
        raise serializers.ValidationError(f'Error filter decode; {filter_info=} {e=}')


class CustomSearchFilter(filters.SearchFilter):
    def get_search_terms(self, request):
        search = super().get_search_terms(request)

        filter_info = get_filter_info(request)
        if filter_info:
            _search = filter_info.get('search')
            if _search:
                return [_search]

        return search


class CustomOrderingFilter(filters.OrderingFilter):

    def get_ordering(self, request, queryset, view):
        ordering = super().get_ordering(request, queryset, view)

        filter_info = get_filter_info(request)
        if filter_info:
            _ordering = filter_info.get('ordering')
            if _ordering:
                return [_ordering]

        return ordering


class CustomFilterBackend(rest_framework.DjangoFilterBackend):
    filterset_base = BaseAdminFilterSet

    def get_filterset_kwargs(self, request, queryset, view):
        data = request.query_params

        filter_info = get_filter_info(request)
        if filter_info:
            _filters = filter_info.get('filters')
            if _filters:
                data = _filters

        return {
            'data': data,
            'queryset': queryset,
            'request': request,
        }
