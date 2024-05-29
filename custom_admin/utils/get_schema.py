from custom_admin.controllers.permissions import CheckPermissions, PermissioinType
from custom_admin.controllers.schema_generator import ViewSetSchemaGenerator


def get_schema(router, request) -> dict:
    sections = {}

    for _prefix, viewset, basename in router.registry:

        has_perm = CheckPermissions(request.user).has_perm(viewset, PermissioinType.VIEW)
        if not has_perm:
            continue

        if has_perm:
            generator = ViewSetSchemaGenerator(viewset, router, basename, request)
            sections[basename] = generator.get_viewset_urls()

    return sections
