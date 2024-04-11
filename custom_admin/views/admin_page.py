import json

from custom_admin.views.template import CUSTOM_ADMIN_TEMPLATE_STRING
from django.conf import settings
from django.template import Context, Template
from django.views import View


class CustomAdminView(View):
    '''
    # Settings in case of h2ttps:
    USE_X_FORWARDED_HOST = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    '''

    template = 'custom_admin/admin_index.html'

    def get(self, request):
        admin_settings = {
            'title': settings.CUSTOM_ADMIN.get('title'),
            'base_admin_url': settings.CUSTOM_ADMIN.get('base_admin_url') or 'admin/',
            'static_prefix': settings.CUSTOM_ADMIN.get('static_prefix') or '/static',
        }

        if not admin_settings.get('backend_prefix'):
            admin_settings['backend_prefix'] = request.build_absolute_uri('/custom_admin/')

        context = {
            'SETTINGS': admin_settings,
            'SETTINGS_JSON': json.dumps(admin_settings),
        }

        template = Template(CUSTOM_ADMIN_TEMPLATE_STRING)
        return template.render(Context(context))
