# Generated by Django 4.2.7 on 2024-04-11 18:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.CharField(max_length=64, verbose_name='Раздел')),
                ('title', models.CharField(blank=True, max_length=64, null=True, verbose_name='Заголовок')),
                ('action_type', models.CharField(choices=[('create', 'Создание'), ('edit', 'Редактирование'), ('action', 'Действие')], max_length=12, verbose_name='Тип действия')),
                ('content', models.JSONField(default=dict, verbose_name='Содержимое действия')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Время совершения действия')),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='admin_actions', to=settings.AUTH_USER_MODEL, verbose_name='Персонал')),
            ],
            options={
                'verbose_name': 'Лог действия администратора',
                'verbose_name_plural': 'Лог действий администраторов',
            },
        ),
    ]
