import logging

from django.conf import settings
from django.utils import translation
from rest_framework.response import Response
from rest_framework.views import APIView

from custom_admin.api.permissions import AdminPermission
from custom_admin.api.serializers import ProfileSerializer
from custom_admin.utils import get_schema

log = logging.getLogger("request")


class GetAdminSectionsAPIView(APIView):
    '''
    Get all scheme for admin frontend
    '''
    throttle_classes = []
    permission_classes = (AdminPermission, )
    router = None

    def get(self, request, *args, **kwargs):
        lang = request.headers.get('Accept-Language') or getattr(settings, 'LANGUAGE_CODE', None) or 'en'
        translation.activate(lang)
        response = Response({
            'sections': get_schema(self.router, request),
            'language': lang,
            'languages': {lang[0]: lang[1] for lang in settings.LANGUAGES},
            'profile': ProfileSerializer(request.user).data,
        })
        return response
