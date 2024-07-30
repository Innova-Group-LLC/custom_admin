import logging

from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext as _
from rest_framework import fields, relations
from rest_framework.exceptions import ValidationError
from rest_framework.fields import empty
from rest_framework.relations import ManyRelatedField, MANY_RELATION_KWARGS

log = logging.getLogger("base-admin-serializer")


def get_str_value(obj):
    if obj:
        try:
            return str(obj)
        except TypeError as e:
            log.error(
                'to_representation error: cant get str from %s with id:%s return None',
                obj.__class__.__name__, obj.id
            )


class AdminManyRelatedField(ManyRelatedField):
    def run_validation(self, data=empty):
        """
            Фиксит проблему (в serializers.ModelSerializer, когда он строит поле
             django.db.models.models.ManyToManyField), когда ставишь потом удаляешь значение,
             необоснованно вызывается исключение "Это поле не может быть пустым"
             при data = [] такого не происходит
        """
        if data is None:
            data = []
        return super().run_validation(data)


class AdminPrimaryKeyRelatedField(relations.PrimaryKeyRelatedField):
    instance = None
    filter_queryset = None
    update_only = None
    create_only = None

    def __init__(self, **kwargs):
        self.filter_queryset = kwargs.pop('filter_queryset', None)
        self.update_only = kwargs.pop('update_only', False)
        self.create_only = kwargs.pop('create_only', False)
        super().__init__(**kwargs)

    @classmethod
    def many_init(cls, *args, **kwargs):
        list_kwargs = {'child_relation': cls(*args, **kwargs)}
        for key in kwargs:
            if key in MANY_RELATION_KWARGS:
                list_kwargs[key] = kwargs[key]

        return AdminManyRelatedField(**list_kwargs)

    def get_attribute(self, instance):
        if self.use_pk_only_optimization() and self.source_attrs:
            try:
                field_name = self.source_attrs[-1]
                attribute_instance = fields.get_attribute(instance, self.source_attrs[:-1])
                value = attribute_instance.serializable_value(field_name)

                if fields.is_simple_callable(value):
                    return value()
                else:
                    return getattr(instance, field_name, None)

            except AttributeError:
                pass

    def to_representation(self, value):
        if self.pk_field is not None:
            return self.pk_field.to_representation(value.pk)

        request = self.context.get('request', None)
        if request and request.GET.get('full_relations'):
            return {"pk": value.pk, "text": get_str_value(value)}

        return value.pk

    def to_internal_value(self, data):
        _id = data
        text = None
        if isinstance(data, dict):
            _id = data.get('pk')
            text = data.get('text')

        if self.pk_field is not None:
            _id = self.pk_field.to_internal_value(_id)
        queryset = self.get_queryset()
        try:
            return queryset.get(pk=_id)

        except ObjectDoesNotExist:
            raise ValidationError(_('The option ‘%(title)s’ is not among the available options.') % {'title': text or id})

        except (TypeError, ValueError):
            self.fail('incorrect_type', data_type=type(_id).__name__)

    def get_queryset(self):
        qs = super().get_queryset()

        if self.filter_queryset:
            form_data = {}
            request = self.context.get('request', None)
            if request:
                form_data = request.data

            qs = self.filter_queryset(qs, form_data, request)

        return qs
