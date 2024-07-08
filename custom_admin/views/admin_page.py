import json

from django.conf import settings
from django.shortcuts import render
from django.template.exceptions import TemplateDoesNotExist
from django.views import View

from custom_admin import VERSION
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

        logo_image = custom_admin.get('logo_image')
        if logo_image and not logo_image.startswith('http'):
            logo_image = request.build_absolute_uri(logo_image)

        favicon_image = custom_admin.get('favicon_image', '/static/custom_admin/favicon.ico')
        if favicon_image and not favicon_image.startswith('http'):
            favicon_image = request.build_absolute_uri(favicon_image)

        backend_prefix = custom_admin.get('backend_prefix', '/custom_admin/')
        if backend_prefix and not backend_prefix.startswith('http'):
            backend_prefix = request.build_absolute_uri(backend_prefix)

        admin_settings = {
            'title': custom_admin.get('title', 'Admin'),
            'logo_image': logo_image,
            'backend_prefix': backend_prefix,
            'favicon_image': favicon_image,
            'version': VERSION,
        }

        context = {
            'SETTINGS': admin_settings,
            'SETTINGS_JSON': json.dumps(admin_settings),
        }

        try:
            return render(request, self.template, context)
        except TemplateDoesNotExist as e:
            raise TemplateDoesNotExist(TEMPLATE_NOT_FOUND.format(template=self.template)) from e
