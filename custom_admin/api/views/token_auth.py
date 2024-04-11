import logging

from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from custom_admin.api.serializers.auth_response import AdminAuthResponseSerializer

logger = logging.getLogger('custom_admin')


class AdminAuthToken(APIView):

    def get_response(self, user, request):
        context = {
            'request': request,
        }
        data = AdminAuthResponseSerializer(user, context=context).data
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        error_response = Response({'non_field_errors': [_('The user is not found or does not have administrator rights.')]}, 401)

        user = get_user_model().objects.filter(username=username).first()
        if not user:
            logger.info('ADMIN BYPASS Login user username:%s not found', username)
            return error_response

        if not user.check_password(password):
            logger.info('ADMIN BYPASS Login user username:%s wrong password', username)
            return error_response

        if not user.is_staff or not user.is_active:
            logger.info('ADMIN BYPASS Login user username:%s not staff or not active', username)
            return error_response

        return self.get_response(user, request)
