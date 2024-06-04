from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class AdminLogType(models.TextChoices):
    CREATE = 'create', _('Create')
    EDIT = 'edit', _('Edit')
    ACTION = 'action', _('Action')


class AdminLog(models.Model):
    staff = models.ForeignKey(
        get_user_model(),
        verbose_name=_('Admin'),
        on_delete=models.PROTECT,
        related_name='admin_actions',
    )
    section = models.CharField(
        _('Section'),
        max_length=64,
    )
    title = models.CharField(
        _('Title'),
        max_length=64,
        blank=True, null=True,
    )
    action_type = models.CharField(
        _('Action type'),
        max_length=12,
        choices=AdminLogType.choices,
    )

    content = models.JSONField(
        verbose_name=_("Log content"), default=dict
    )
    created_at = models.DateTimeField(
        verbose_name=_('Time of action'), default=timezone.now,
    )

    class Meta:
        verbose_name = _('Admin action log')
        verbose_name_plural = _('Admin action logs')

    def __str__(self):
        return f'{self.get_action_type_display()} #{self.id} {self.staff.username}'
