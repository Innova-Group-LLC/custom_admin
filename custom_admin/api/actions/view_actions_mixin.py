import asyncio as aio
import logging
from typing import Awaitable, Callable

from asgiref.sync import sync_to_async
from django.http import HttpResponse
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from custom_admin.api.actions.action_result import ActionResult
from custom_admin.api.actions.delete_action import delete_action
from custom_admin.controllers import AdminLogManager

log = logging.getLogger('admin')


class ActionSerializer(serializers.Serializer):
    pks = serializers.ListField(child=serializers.CharField(), required=False)
    form_data = serializers.JSONField(required=False, allow_null=True)

    send_to_all = serializers.BooleanField(default=False)
    relfilterid = serializers.CharField(required=False)
    relfilter = serializers.CharField(required=False)


class AdminActionMixIn:

    actions = [
        delete_action,
    ]

    @action(detail=False, methods=['post'], url_path='send_action/(?P<action_name>.+)')
    async def send_action(self, request, action_name, pk=None):
        serializer = ActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        pks = serializer.validated_data['pks']
        send_to_all = serializer.validated_data['send_to_all']
        form_data = serializer.validated_data['form_data']

        actions_dict = {
            action.__name__: action
            for action in self.actions
        }

        if action_name not in actions_dict:
            return Response(f'View {self.get_view_viewname()} doesnt have action "{action_name}"', status=400)

        qs = await sync_to_async(self.get_queryset)()
        qs = await sync_to_async(self.filter_queryset)(qs)

        if not send_to_all:
            qs = qs.filter(pk__in=pks)

        relfilterid = serializer.validated_data.get('relfilterid')
        relfilter = serializer.validated_data.get('relfilter')
        if relfilterid and relfilter:
            qs = qs.filter(**{relfilter: relfilterid})

        action_fn: Awaitable[Callable] = actions_dict[action_name]
        if not aio.iscoroutinefunction(action_fn):
            raise Exception(
                f'Decorator "admin_action" is required for {self.get_view_viewname()}.{action_name} (is not coroutine function)'
            )

        actions_result = await action_fn(self, request, qs, form_data)

        if isinstance(actions_result, ActionResult):
            action_response = actions_result.to_response()

        elif isinstance(actions_result, (tuple, list)):
            action_messages, code = actions_result

            if isinstance(action_messages, (str)) or action_messages.__class__.__name__ == '__proxy__':
                action_messages = [action_messages]

            action_response = Response({'action_messages': action_messages}, status=code)

        elif isinstance(actions_result, (Response, HttpResponse)):
            action_response = actions_result

        else:
            raise NotImplementedError(f'actions_result type {actions_result.__class__} is not implemented')

        await sync_to_async(self.log_action)(action_name, actions_dict[action_name].short_description, request)
        return action_response

    def log_action(self, action_name: str, short_description: str, request):
        AdminLogManager(self.request.user).register_action(
            action_name, short_description, self, request
        )
