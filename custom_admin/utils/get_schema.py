from custom_admin.controllers.schema_generator import ViewSetSchemaGenerator


def get_schema(router, request) -> dict:
    sections = {}

    for _prefix, viewset, basename in router.registry:

        has_perm = True
        for perm in viewset.permission_classes:
            if not perm().has_permission(request, viewset):
                has_perm = False
                break

        if has_perm:
            generator = ViewSetSchemaGenerator(viewset, router, basename, request)
            sections[basename] = generator.get_viewset_urls()

    return sections
