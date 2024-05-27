import json

from django.conf import os, settings
from django.shortcuts import render
from django.template.exceptions import TemplateDoesNotExist
from django.views import View

from custom_admin.utils import get_schema

TEMPLATE_NOT_FOUND = '''
Custom admin cannot find template "{template}".
Make sure settings.TEMPLATES contains 'APP_DIRS': True
'''


class CustomAdminView(View):
    '''
    # Settings in case of h2ttps:
    USE_X_FORWARDED_HOST = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    '''

    template = 'custom_admin/admin_index.html'

    def get(self, request):
        custom_admin = getattr(settings, 'CUSTOM_ADMIN', {})

        admin_settings = {
            'title': custom_admin.get('title', 'Admin'),
            'backend_prefix': custom_admin.get('backend_prefix'),
        }

        if not admin_settings.get('backend_prefix'):
            admin_settings['backend_prefix'] = request.build_absolute_uri('/custom_admin/')

        context = {
            'SETTINGS': admin_settings,
            'SETTINGS_JSON': json.dumps(admin_settings),
        }

        try:
            return render(request, self.template, context)
        except TemplateDoesNotExist as e:
            raise TemplateDoesNotExist(TEMPLATE_NOT_FOUND.format(template=self.template)) from e
