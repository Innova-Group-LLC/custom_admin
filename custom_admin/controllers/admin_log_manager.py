import logging

from django.contrib.auth import get_user_model
from django.db.models.fields.files import ImageFieldFile

from custom_admin.models import AdminLog
from custom_admin.models.admin_log import AdminLogType

log = logging.getLogger("custom_admin")


class AdminLogManager:
    staff: get_user_model()

    def __init__(self, staff):
        self.staff = staff

    def register_create(self, serializer, validated_data, created_instance) -> AdminLog:
        content = {
            k: str(v)
            for k, v in validated_data.items()
        }

        admin_log = AdminLog.objects.create(
            staff=self.staff,
            section=serializer.context['viewname'],
            action_type=AdminLogType.CREATE,
            content=content,
            title=str(created_instance)[:63],
        )
        log.info(
            'ADMIN %s #%s CREATED "%s" #%s viewname:%s log:%s',
            self.staff.username, self.staff.id,
            created_instance._meta.verbose_name, created_instance.id,
            serializer.context['viewname'], admin_log.id,
            extra={'validated_data': validated_data}
        )

    @staticmethod
    def get_image_safe(image):
        if image and hasattr(image, 'url'):
            return image.url
        return None

    def check_equal(self, original_value, new_value):
        if isinstance(original_value, ImageFieldFile) and isinstance(new_value, ImageFieldFile):
            return self.get_image_safe(original_value) != self.get_image_safe(new_value)
        else:
            return original_value != new_value

    @staticmethod
    def get_field_value(instance, k):
        value = getattr(instance, k, None)
        if value.__class__.__name__ == 'ManyRelatedManager':
            return list(value.all().values_list('id', flat=True))

        return value

    def register_update(self, serializer, data_before_update, validated_data, updated_instance) -> AdminLog:
        content = {}
        for k in validated_data.keys():
            original_value = data_before_update.get(k)
            new_value = self.get_field_value(updated_instance, k)

            if self.check_equal(original_value, new_value):
                content[k] = {'from': str(original_value), 'to': str(new_value)}

        if not content:
            return

        admin_log = AdminLog.objects.create(
            staff=self.staff,
            section=serializer.context['viewname'],
            action_type=AdminLogType.EDIT,
            content=content,
            title=str(updated_instance)[:63],
        )
        log.info(
            'ADMIN %s #%s UPDATE "%s" #%s viewname:%s log:%s',
            self.staff.username, self.staff.id,
            updated_instance._meta.verbose_name, updated_instance.id,
            serializer.context['viewname'], admin_log.id,
            extra={'validated_data': validated_data}
        )
        return admin_log

    def register_action(self, action_name, short_description, view, request) -> AdminLog:
        admin_log = AdminLog.objects.create(
            staff=self.staff,
            section=view.get_view_viewname(),
            action_type=AdminLogType.ACTION,
            content=request.data,
            title=short_description,
        )
        log.info(
            'ADMIN %s #%s ACTION "%s" admin_log:%s request.data:%s short_description:%s',
            self.staff.username, self.staff.id, action_name, admin_log.section, request.data, short_description,
        )
        return admin_log
