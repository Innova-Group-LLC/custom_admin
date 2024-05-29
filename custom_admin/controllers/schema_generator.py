import typing

from django.conf import settings
from django.utils.translation import gettext as _
from django_filters.utils import get_model_field

from custom_admin.api.action_functions import ACTION_ATTRIBUTES
from custom_admin.api.serializers.base_serializer import AdminModelSerializer
from custom_admin.api.viewset_info import AdminViewSetInfo
from custom_admin.controllers.filters_schema import (
    ModelFieldException,
    get_filters_class_data,
    get_filters_fields_data,
)
from custom_admin.controllers.permissions import CheckPermissions, PermissioinType


class ViewSetSchemaGenerator:
    viewset = None
    router = None
    basename = None
    request = None
    model = None

    def __init__(self, viewset, router, basename, request):
        self.viewset = viewset
        self.router = router
        self.basename = basename
        self.request = request

        if hasattr(self.viewset, 'get_model'):
            self.model = viewset.get_model()

    def _get_inline_data(self, initkwargs: dict) -> typing.Optional[dict]:
        inline_type = initkwargs.get('inline_type')

        if inline_type is None:
            return

        filterset_fields = {}
        filterset_class = initkwargs.get('filterset_class')
        if filterset_class is not None:
            filterset_fields = get_filters_class_data(None, filterset_class, self.request)

        return {
            'inline_type': inline_type,
            'filterset_fields': filterset_fields,
            'actions': self._get_actions_info(initkwargs.get('actions', [])),
        }

    def _generate_view_data(self, route, lookup) -> typing.Union[str, dict]:
        'Its for spicific method: user-detail or user-list'

        mappings = self.router.get_method_map(self.viewset, route.mapping)

        regex = route.url.format(
            prefix=self.basename,
            lookup=lookup,
            trailing_slash=self.router.trailing_slash
        )

        if not self.basename and regex[:2] == '^/':
            regex = '^' + regex[2:]

        initkwargs = route.initkwargs.copy()
        initkwargs.update({
            'detail': route.detail,
        })

        name = initkwargs.get('name', route.name.format(basename=self.basename))
        name = _(name)

        mappings_info = {}
        for method, method_name in mappings.items():
            has_perm = CheckPermissions(self.request.user).has_action_perm(self.viewset, method_name)
            if has_perm:
                mappings_info[method] = method_name

        url_data = {
            'slug': route.name.format(basename=self.basename),
            'mapping': mappings_info,
            'name': name,
            'detail': route.detail,
        }

        inline_data = self._get_inline_data(initkwargs)
        if inline_data is not None:
            url_data.update(inline_data)

        return name, url_data

    def _get_filters_data(self):
        filters_data = []

        if self.model:
            filters = getattr(self.viewset, 'filterset_fields', None)
            if filters:
                try:
                    filters_data = get_filters_fields_data(self.model, filters)
                except ModelFieldException as e:
                    raise ModelFieldException(f'View {self.viewset.__name__}: {e}')

            filter_class = getattr(self.viewset, 'filter_class', None) or getattr(self.viewset, 'filterset_class', None)
            if filter_class:
                filters_data = get_filters_class_data(self.model, filter_class, self.request)

        return filters_data

    def _get_serializer_info(self):
        serializer = None
        serializer_info = None

        meta = self.viewset.metadata_class()
        if hasattr(self.viewset, 'get_serializer_class') and self.viewset.get_serializer_class():
            serializer = self.viewset.get_serializer_class()()
            try:
                serializer_info = meta.get_serializer_info(serializer)
            except Exception as e:
                raise Exception(f'Error in {self.viewset.__name__}: {e}')

            if not issubclass(serializer.__class__, (AdminModelSerializer,)):
                raise Exception(
                    'Admin serializer {} must be inherited from AdminModelSerializer'.format(
                        serializer.__class__.__name__
                    )
                )

            if 'id' not in serializer_info.keys():
                raise Exception(
                    f'Make sure that {serializer.__class__.__name__} have id field'
                )

        return serializer, serializer_info

    def _get_list_display(self, serializer_info, serializer):
        list_display = getattr(self.viewset, 'list_display', None)
        if list_display:
            if 'id' not in list_display:
                list_display = list(list_display) + ['id']

            for field_display in list_display:
                if field_display not in serializer_info.keys():
                    raise Exception(
                        f'Field "{field_display}" from {self.viewset.__name__}.list_display not presented in {serializer.__class__.__name__}'
                    )
        return list_display

    def _get_search_fields(self):
        result_search_fields = []
        search_fields = getattr(self.viewset, 'search_fields', [])
        if search_fields:
            if self.model:
                for search_field in search_fields:
                    field = get_model_field(self.model, search_field)
                    if field:
                        name = field.verbose_name
                        if name == 'ID':
                            name = f'{_(field.model._meta.verbose_name)} ID'
                        result_search_fields.append(_(name))
                    else:
                        result_search_fields.append(_(search_field))
            else:
                result_search_fields = search_fields

        return result_search_fields

    def _get_actions_info(self, view_actions) -> dict:
        actions = {}

        has_perm = CheckPermissions(self.request.user).has_perm(self.viewset, PermissioinType.ACTIONS)
        if not has_perm:
            return actions

        for action in view_actions:
            name = getattr(action, 'short_description', action.__name__)
            actions[action.__name__] = {'name': name}

            for attr in ACTION_ATTRIBUTES:
                actions[action.__name__][attr] = getattr(action, attr, None)

            form_serializer = getattr(action, 'form_serializer', None)
            if form_serializer:
                meta = self.viewset.metadata_class()
                serializer_info = meta.get_serializer_info(form_serializer())
                actions[action.__name__]['form_serializer'] = serializer_info
        return actions

    def _get_translations_info(self, serializer):
        try:
            from modeltranslation.translator import NotRegistered, translator
        except ModuleNotFoundError:
            return {}

        if not self.model:
            return {}

        result = {}
        try:
            for field in translator.get_options_for_model(self.model).fields:
                result[field] = []
                for lang_slug, lang_translation in settings.LANGUAGES:
                    result[field].append({
                        'slug': f'{field}_{lang_slug}',
                        'lang_slug': lang_slug,
                        'lang_translation': str(lang_translation),
                    })

            from custom_admin.api.serializers import TranslatedModelSerializer
            if not isinstance(serializer, TranslatedModelSerializer):
                raise ModelFieldException(f'Serializer {serializer.__class__.__name__} has translations, but not instance of TranslatedModelSerializer')

        except NotRegistered:
            pass
        return result


    def get_viewset_urls(self) -> dict:
        viewset_urls = {}

        title = str(_(self.viewset.get_view_title()))
        filters_data = self._get_filters_data()
        serializer, serializer_info = self._get_serializer_info()
        list_display = self._get_list_display(serializer_info, serializer)
        search_fields = self._get_search_fields()

        related_inlines = []
        if hasattr(self.viewset, 'get_related_inlines'):
            for related_inline in self.viewset.get_related_inlines():
                has_perm = CheckPermissions(self.request.user).has_perm_viewname(
                    viewname=related_inline.viewset_name,
                    perm_type=PermissioinType.VIEW,
                )
                if has_perm:
                    related_inlines.append(related_inline.asdict())

        meta_data = {
            'serializer': serializer_info,
            'search_fields': search_fields,
            'ordering_fields': getattr(self.viewset, 'ordering_fields', []),
            'related_inlines': related_inlines,
            'field_groups': getattr(serializer.Meta, 'groups', None) if serializer else None,
            'filterset_fields': filters_data,
            'filds_list': list_display,
            'fixed_columns': getattr(self.viewset, 'fixed_columns', []),
            'actions': self._get_actions_info(getattr(self.viewset, "actions", [])),
            'translations': self._get_translations_info(serializer),
        }

        lookup = self.router.get_lookup_regex(self.viewset)
        viewset_urls = {
            'viewname': self.viewset.get_view_viewname(),
            'lookup': lookup,
            'title': str(title),
            'routers': {},
            'hide_in_navigation': self.viewset.hide_in_navigation,
            'icon': self.viewset.icon,
            'meta': meta_data,
        }

        viewset_info: AdminViewSetInfo = self.viewset._info
        viewset_urls.update(viewset_info.asdict())

        routes = self.router.get_routes(self.viewset)
        for route in routes:
            route_name, url_data = self._generate_view_data(route, lookup)
            viewset_urls['routers'][route_name] = url_data

        return viewset_urls
