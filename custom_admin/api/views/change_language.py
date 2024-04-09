from rest_framework.response import Response
from rest_framework.views import APIView

from custom_admin.api.permissions import AdminPermission


class ChangeLanguageAPIView(APIView):
    throttle_classes = []
    permission_classes = (AdminPermission, )

    def post(self, request, *args, **kwargs):
        user = request.user
        user.language = request.data['language']
        user.save(update_fields=['language'])
        return Response({
            'user.type': user.__class__.__name__,
            'user.id': user.id,
            'user.language': user.language,
        })
