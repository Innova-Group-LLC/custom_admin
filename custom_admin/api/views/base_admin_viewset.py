import asyncio as aio
import logging
import typing

from asgiref.sync import sync_to_async
from django.db.models.fields.related_descriptors import ForwardManyToOneDescriptor, ManyToManyDescriptor
from django.utils.decorators import classonlymethod
from django.utils.translation import gettext as _
from rest_framework import mixins, serializers, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import JSONParser, MultiPartParser

from custom_admin.api.actions import AdminActionMixIn, export_csv_action
from custom_admin.api.backends import CustomFilterBackend, CustomOrderingFilter, CustomSearchFilter
from custom_admin.api.inline_relation import RelatedInline
from custom_admin.api.inlines import ViewActionsInlineMixIn
from custom_admin.api.permissions import AdminPermission
from custom_admin.controllers.custom_metadata import CustomMetadata
from custom_admin.utils.async_mixin import AsyncMixin

log = logging.getLogger('admin')


class AdminPaginator(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'limit'


class BaseAdminDataViewSet(ViewActionsInlineMixIn, viewsets.ViewSet):
    icon: typing.Optional[str] = None  # # https://pictogrammers.com/library/mdi/
    hide_in_navigation: typing.Optional[bool] = None

    throttle_classes = []
    parser_classes = (MultiPartParser, JSONParser)
    metadata_class = CustomMetadata
    permission_classes = (AdminPermission, )

    viewname = None
    title = None

    @classmethod
    def get_model(cls) -> typing.Optional[typing.Any]:
        return None

    @classmethod
    def get_view_viewname(cls):
        viewname = getattr(cls, 'viewname', None)
        if viewname:
            return viewname

        if hasattr(cls, 'get_model'):
            view_model = cls.get_model()
            if view_model:
                return view_model.__name__.lower()

        return cls.__name__.lower()

    @classmethod
    def get_view_title(cls):
        viewname = getattr(cls, 'title', None)
        if viewname:
            return viewname

        if hasattr(cls, 'get_model'):
            view_model = cls.get_model()
            if view_model:
                return _(view_model._meta.verbose_name_plural)

        return cls.__name__.lower()

    @classonlymethod
    def as_view(cls, *args, **initkwargs):
        # parameters of rest_framework.decorators.action
        initkwargs.pop('type', None)
        initkwargs.pop('filterset_class', None)
        view = super().as_view(*args, **initkwargs)

        async def async_view(*args, **kwargs):
            # wait for the `dispatch` method
            return await view(*args, **kwargs)
        async_view.csrf_exempt = True
        return async_view

    async def dispatch(self, request, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers  # deprecate?

        try:
            # MODIFIED HERE
            await sync_to_async(self.initial)(
                request, *args, **kwargs
            )

            if request.method.lower() in self.http_method_names:
                handler = getattr(
                    self, request.method.lower(),
                    self.http_method_not_allowed
                )
            else:
                handler = self.http_method_not_allowed

            handler_kwargs = getattr(handler, 'kwargs', {})
            handler_inline_type = handler_kwargs.get('inline_type')
            if handler_inline_type is not None:

                async_handle_inline = self.handle_inline
                if not aio.iscoroutinefunction(async_handle_inline):
                    async_handle_inline = sync_to_async(async_handle_inline)

                response = await async_handle_inline(handler, request, handler_kwargs, *args, **kwargs)
            else:
                if not aio.iscoroutinefunction(handler):
                    handler = sync_to_async(handler)
                response = await handler(request, *args, **kwargs)

        except Exception as exc:
            response = self.handle_exception(exc)

        self.response = self.finalize_response(request, response, *args, **kwargs)
        return self.response


class BaseAdmin(AdminActionMixIn, BaseAdminDataViewSet, AsyncMixin):
    '''
    serializer_class is optional, will be used all fields by default or
    you can set serializer_fields
    '''
    pagination_class = AdminPaginator
    filter_backends = [
        CustomSearchFilter, CustomOrderingFilter, CustomFilterBackend
    ]
    search_fields = ['id']
    ordering_fields = ['id']
    ordering = ['-id']
    filterset_fields = []

    fixed_columns = ('id',)

    # Set None for diplay all fields
    filds_list = ['id']

    related_inlines: typing.List[RelatedInline] = []

    @classmethod
    def get_related_inlines(cls) -> typing.List[dict]:
        result = []
        for i, inline in enumerate(cls.related_inlines):

            if not isinstance(inline, RelatedInline):
                raise serializers.ValidationError(f'View {cls.__name__}.related_inlines[{i}] error: is not an instance of RelatedInline')

            inline.validate(cls, i)
            result.append(inline.asdict())

        return result

    @classmethod
    def get_model(cls) -> typing.Optional[typing.Any]:
        return cls.get_serializer_class().Meta.model

    def get_queryset(self):
        qs = super().get_queryset()

        relfilterid = self.request.query_params.get('relfilterid')
        relfilter = self.request.query_params.get('relfilter')
        if relfilterid and relfilter:
            qs = qs.filter(**{relfilter: relfilterid})

        return qs

    def get_serializer_context(self):
        '''
        Если передаются query_params c id объекта, то добавляем его в контекст сериализатора
        '''
        ctx = {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }
        relfilterid = self.request.query_params.get('relfilterid')
        relfilter = self.request.query_params.get('relfilter')
        if relfilterid and relfilter:
            relobject = None
            try:
                rel_model_descriptor = getattr(self.get_model(), relfilter)
                if isinstance(rel_model_descriptor, ManyToManyDescriptor):
                    relobject = rel_model_descriptor.rel.related_model.objects.get(id=relfilterid)
                if isinstance(rel_model_descriptor, ForwardManyToOneDescriptor):
                    relobject = rel_model_descriptor.field.related_model.objects.get(id=relfilterid)
                ctx.update({'relobject': relobject})
            except Exception:
                pass

        ctx.update({'viewname': self.get_view_viewname()})
        return ctx

    @classmethod
    def get_serializer_class(cls):
        if hasattr(cls, 'serializer_class'):
            serializer_class = getattr(cls, 'serializer_class')
            if serializer_class:
                return serializer_class

        from custom_admin.api.serializers import AdminModelSerializer

        class GenericAdminSerializer(AdminModelSerializer):
            class Meta:
                model = cls.queryset.model
                fields = getattr(cls, 'serializer_fields', '__all__')
                ref_name = cls.queryset.model.__name__

        cls.serializer_class = GenericAdminSerializer
        return cls.serializer_class


class WithoutCreateBaseAdminViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
    BaseAdmin
):
    pass


class WithoutUpdateBaseAdminViewSet(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
    BaseAdmin
):
    pass


class BaseAdminViewSet(mixins.CreateModelMixin, WithoutCreateBaseAdminViewSet):
    pass


class ReadOnlyBaseAdminViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
    BaseAdmin
):
    actions = [export_csv_action]


class ListBaseAdminViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
    BaseAdmin
):
    actions = [export_csv_action]
