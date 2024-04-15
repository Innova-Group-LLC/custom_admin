from django.core.management.base import BaseCommand

VIEWSET_INFO = '''- {title: <35} {view_slug: <25} model:{model}'''


class Command(BaseCommand):
    def handle(self, *args, **options):
        from custom_admin.utils.register_admin_viewsets import _ADMIN_VIEWS

        if not _ADMIN_VIEWS:
            self.stdout.write(
                self.style.ERROR('settings.ADMIN_URLS is empty')
            )

        groups = {}
        for viewset in _ADMIN_VIEWS.values():
            groups[viewset._info.group_slug] = viewset._info.title

        for group_slug, group_title in groups.items():
            self.stdout.write(f'\n"{group_title}" {group_slug}')

            for view_slug, viewset in _ADMIN_VIEWS.items():
                if viewset._info.group_slug != group_slug:
                    continue

                model = None
                if hasattr(viewset, 'get_model'):
                    model = viewset.get_model()

                if model:
                    model = model.__name__

                line = VIEWSET_INFO.format(
                    view_slug=view_slug,
                    model=model,
                    title=str(viewset.get_view_title()),
                )
                self.stdout.write(
                    self.style.SUCCESS(line)
                )
