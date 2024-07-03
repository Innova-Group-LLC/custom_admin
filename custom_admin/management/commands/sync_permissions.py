from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from custom_admin.controllers.permissions import CheckPermissions


class Command(BaseCommand):
    def handle(self, *args, **options):
        from custom_admin.utils.register_admin_viewsets import _ADMIN_VIEWS

        if not _ADMIN_VIEWS:
            self.stdout.write(
                self.style.ERROR('settings.ADMIN_URLS is empty')
            )

        for viewset in _ADMIN_VIEWS.values():
            permissions = CheckPermissions.get_all_permissions(viewset)
            for codename, info in permissions.items():

                perm = Permission.objects.filter(codename=codename).first()
                if not perm:
                    perm = Permission.objects.create(
                        codename=codename,
                        name=info['title'],
                        content_type=ContentType.objects.get_for_model(Permission),
                    )
                    self.stdout.write(self.style.SUCCESS(f'- "{perm.name}" created'))

                elif perm.name != info['title']:
                    perm.name = info['title']
                    perm.save(update_fields=['name'])

        self.stdout.write('Permissions sync completed')
