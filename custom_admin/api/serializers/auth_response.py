from rest_framework import serializers
from rest_framework.authtoken.models import Token

from django.contrib.auth import get_user_model

from custom_admin.api.serializers.base_serializer import AdminModelSerializer


class AdminAuthResponseSerializer(AdminModelSerializer):
    token = serializers.SerializerMethodField()
    language = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = [
            'pk',
            'username',
            'token',
            'language',
        ]

    def get_token(self, user):
        token, _ = Token.objects.get_or_create(user=user)
        return token.key

    def get_language(self, user):
        return getattr(user, 'language', 'en')
