import logging
import typing
from datetime import datetime, time

from django.conf import settings
from django.utils.decorators import classonlymethod
from rest_framework.response import Response

from custom_admin.api.backends import get_filter_info
from custom_admin.api.inlines.interfaces import InlineResultInterface
from custom_admin.controllers import AdminLogManager

DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'

log = logging.getLogger("admin-actions")


class InlineError(Exception):
    pass


class ViewActionsInlineMixIn:
    """
    Handler for action with type='Inline'
    from rest_framework.decorators import action

    Action decorator must contain
    - inline_type: InlinesType
    - filterset_class: instance of BaseAdminFilterSet
    - actions: list of funcs
    """

    def get_filters(self, filterset_class, request) -> typing.Dict[str, typing.Any]:
        if filterset_class is None:
            return {}

        filters = {}
        filter_info = get_filter_info(request)
        if filter_info:
            filters = filter_info.get('filters') or {}

        for filter_key in filters.keys():
            _filter = filters[filter_key]

            if isinstance(_filter, dict):
                if 'from' in _filter:
                    d = datetime.strptime(_filter.get('from'), DATETIME_FORMAT)
                    _filter['from'] = datetime.combine(d, time.min)

                if 'to' in _filter:
                    d = datetime.strptime(_filter.get('to'), DATETIME_FORMAT)
                    _filter['to'] = datetime.combine(d, time.max)

        return filters

    @classonlymethod
    def as_view(cls, *args, **initkwargs):
        # parameters of rest_framework.decorators.action
        initkwargs.pop('inline_type', None)
        initkwargs.pop('filterset_class', None)
        initkwargs.pop('actions', None)
        return super().as_view(*args, **initkwargs)

    def perform_action(self, view, request, handler_result, inline_action, actions):
        for action in actions:
            if action.__name__ == inline_action:
                action_result = action(view, request, handler_result)
                AdminLogManager(self.request.user).register_action(
                    action.__name__, action.short_description, self, request
                )
                return action_result

        return Response(f'Action {action.__name__} not found', status=400)

    def handle_inline(self, view_handler, request, handler_kwargs, *args, **kwargs) -> Response:
        # inline_type = handler_kwargs.get('inline_type')

        filterset_class = handler_kwargs.get('filterset_class')

        permission_classes = handler_kwargs.get('permission_classes')
        for permission_class in permission_classes:
            if not permission_class().has_permission(request, None):
                return Response('You don\'t have access', status=401)

        filters = self.get_filters(filterset_class, request)

        page = request.GET.get('page', 1)
        page_size = request.GET.get('limit', settings.REST_FRAMEWORK['PAGE_SIZE'])

        inline_action = request.GET.get('inline_action')

        pk = kwargs.pop('pk', None)

        try:
            handler_result: typing.Optional[InlineResultInterface] = view_handler(request, pk, filters, page, page_size, inline_action, *args, **kwargs)
        except Exception as e:
            log.exception('Action error:"%s"', str(e))
            raise InlineError(f'Action error: {e}') from e

        # Inlines can have actions as export_csv_inline
        if inline_action:
            return self.perform_action(view_handler, request, handler_result, inline_action, handler_kwargs.get('actions'))

        if handler_result is None:
            return Response()

        if not issubclass(handler_result.__class__, InlineResultInterface):
            raise InlineError(f'Action view "{view_handler.__name__}" must InlineResultInterface or None; result:{handler_result}')

        return Response(handler_result.asdict())
