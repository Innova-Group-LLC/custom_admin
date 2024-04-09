import logging

from dj_rest_auth.app_settings import api_settings
from dj_rest_auth.jwt_auth import set_jwt_cookies
from dj_rest_auth.utils import jwt_encode
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger('custom_admin')


class AdminAuthToken(APIView):

    @staticmethod
    def get_response_serializer():
        if api_settings.USE_JWT:

            if api_settings.JWT_AUTH_RETURN_EXPIRATION:
                response_serializer = api_settings.JWT_SERIALIZER_WITH_EXPIRATION
            else:
                response_serializer = api_settings.JWT_SERIALIZER

        else:
            response_serializer = api_settings.TOKEN_SERIALIZER
        return response_serializer

    def get_response(self, user, request):
        access_token, refresh_token = jwt_encode(user)
        serializer_class = self.get_response_serializer()

        if api_settings.USE_JWT:
            from rest_framework_simplejwt.settings import api_settings as jwt_settings
            access_token_expiration = (timezone.now() + jwt_settings.ACCESS_TOKEN_LIFETIME)
            refresh_token_expiration = (timezone.now() + jwt_settings.REFRESH_TOKEN_LIFETIME)
            return_expiration_times = api_settings.JWT_AUTH_RETURN_EXPIRATION
            auth_httponly = api_settings.JWT_AUTH_HTTPONLY

            data = {
                'user': user,
                'access': access_token,
            }

            if not auth_httponly:
                data['refresh'] = refresh_token
            else:
                # Wasnt sure if the serializer needed this
                data['refresh'] = ""

            if return_expiration_times:
                data['access_expiration'] = access_token_expiration
                data['refresh_expiration'] = refresh_token_expiration

            serializer = serializer_class(
                instance=data,
                context={'request': request},
            )
        elif self.token:
            serializer = serializer_class(
                instance=self.token,
                context={'request': request},
            )
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

        data = serializer.data

        response = Response(data, status=status.HTTP_200_OK)
        if api_settings.USE_JWT:
            set_jwt_cookies(response, access_token, refresh_token)
        return response


    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        error_response = Response({'non_field_errors': ['Пользователь не найден или не имеет прав']}, 401)

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
