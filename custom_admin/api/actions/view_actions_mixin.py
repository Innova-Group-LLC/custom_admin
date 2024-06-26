import asyncio as aio
import logging

from asgiref.sync import sync_to_async
from django.http import HttpResponse
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from custom_admin.api.actions.delete_action import delete_action
from custom_admin.api.actions.export_csv_action import export_csv_action
from custom_admin.controllers import AdminLogManager

log = logging.getLogger('admin')


class ActionSerializer(serializers.Serializer):
    ids = serializers.ListField(child=serializers.CharField(), required=False)
    form_data = serializers.JSONField(required=False, allow_null=True)

    send_to_all = serializers.BooleanField(default=False)
    relfilterid = serializers.CharField(required=False)
    relfilter = serializers.CharField(required=False)


class AdminActionMixIn:

    actions = [
        delete_action, export_csv_action,
    ]

    @action(detail=False, methods=['post'], url_path='send_action/(?P<action_name>.+)')
    async def send_action(self, request, action_name, pk=None):
        serializer = ActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ids = serializer.validated_data['ids']
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
            qs = qs.filter(pk__in=ids)

        relfilterid = serializer.validated_data.get('relfilterid')
        relfilter = serializer.validated_data.get('relfilter')
        if relfilterid and relfilter:
            qs = qs.filter(**{relfilter: relfilterid})

        action_fn = actions_dict[action_name]
        if not aio.iscoroutinefunction(action_fn):
            action_fn = sync_to_async(action_fn)

        actions_result = await action_fn(self, request, qs, form_data)

        if isinstance(actions_result, (tuple, list)):
            action_messages, code = actions_result

            if isinstance(action_messages, (str)) or action_messages.__class__.__name__ == '__proxy__':
                action_messages = [action_messages]

            action_request = Response({'action_messages': action_messages}, status=code)

        elif isinstance(actions_result, (Response, HttpResponse)):
            action_request = actions_result

        else:
            raise NotImplementedError(f'actions_result type {actions_result.__class__} is not implemented')

        await sync_to_async(self.log_action)(action_name, actions_dict[action_name].short_description, request)
        return action_request

    def log_action(self, action_name: str, short_description: str, request):
        AdminLogManager(self.request.user).register_action(
            action_name, short_description, self, request
        )
