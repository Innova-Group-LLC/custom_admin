from django.utils.functional import lazy
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from custom_admin.api import filters as admin_filters
from custom_admin.models import AdminLog
from custom_admin.api.serializers.base_serializer import AdminModelSerializer
from custom_admin.api.views.base_admin_viewset import WithoutCreateBaseAdminViewSet


def get_views_choices():
    from custom_admin.utils.register_admin_viewsets import _ADMIN_VIEWS
    return [
        (viewname, f'{view._info.title} - {view.get_view_title()}')
        for viewname, view in _ADMIN_VIEWS.items()
    ]


class AdminLogFilterSet(admin_filters.BaseAdminFilterSet):
    section = admin_filters.ChoiceFilter(
        label=_('Раздел'), choices=lazy(get_views_choices, tuple),
    )

    class Meta:
        model = AdminLog
        fields = (
            'section', 'staff', 'action_type', 'created_at',
        )


class AdminLogAdminSerializer(AdminModelSerializer):
    section = serializers.SerializerMethodField(label=_('Раздел'))

    class Meta:
        model = AdminLog
        fields = '__all__'
        read_only_fields = (
            'content', 'created_at', 'section', 'action_type', 'staff', 'title',
        )

    def get_section(self, obj):
        from custom_admin.utils.register_admin_viewsets import _ADMIN_VIEWS
        view = _ADMIN_VIEWS.get(obj.section)
        if not view:
            return obj.section

        return f'{view._info.title} - {view.get_view_title()}'


class AdminLogAdminViewSet(WithoutCreateBaseAdminViewSet):
    queryset = AdminLog.objects.all()
    serializer_class = AdminLogAdminSerializer
    search_fields = ['id', 'staff__username', 'title']
    filterset_class = AdminLogFilterSet
    list_display = [
        'id',
        'staff',
        'action_type',
        'section',
        'title',
        'created_at',
    ]
    ordering_fields = ['id', 'staff', 'section', 'action_type', 'title']
