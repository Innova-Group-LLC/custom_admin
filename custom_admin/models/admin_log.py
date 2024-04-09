from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class AdminLogType(models.TextChoices):
    CREATE = 'create', _('Создание')
    EDIT = 'edit', _('Редактирование')
    ACTION = 'action', _('Действие')


class AdminLog(models.Model):
    staff = models.ForeignKey(
        get_user_model(),
        verbose_name=_('Персонал'),
        on_delete=models.PROTECT,
        related_name='admin_actions',
    )
    section = models.CharField(
        _('Раздел'),
        max_length=64,
    )
    title = models.CharField(
        _('Заголовок'),
        max_length=64,
        blank=True, null=True,
    )
    action_type = models.CharField(
        _('Тип действия'),
        max_length=12,
        choices=AdminLogType.choices,
    )

    content = models.JSONField(
        verbose_name=_("Содержимое действия"), default=dict
    )
    created_at = models.DateTimeField(
        verbose_name=_('Время совершения действия'), default=timezone.now,
    )

    class Meta:
        verbose_name = _('Лог действия администратора')
        verbose_name_plural = _('Лог действий администраторов')

    def __str__(self):
        return f'{self.get_action_type_display()} #{self.id} {self.staff.username}'
