from django.contrib.auth import get_user_model

from custom_admin.api.serializers.base_serializer import AdminModelSerializer


class ProfileSerializer(AdminModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            'pk',
            'username',
        ]
