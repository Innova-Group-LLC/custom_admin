import logging

from django.db import models
from modeltranslation.translator import translator
from modeltranslation.utils import get_translation_fields
from rest_framework import relations, serializers

from backend.fields import models as custom_model_fields
from custom_admin.api import fields
from custom_admin.api import fields as admin_fields
from custom_admin.controllers import AdminLogManager

log = logging.getLogger("custom_admin")


class AdminFieldsMixin:
    serializer_related_field = fields.AdminPrimaryKeyRelatedField
    serializer_related_to_field = relations.SlugRelatedField
    serializer_choice_field = fields.AdminChoiceField

    serializer_field_mapping = serializers.ModelSerializer.serializer_field_mapping
    serializer_field_mapping[models.FileField] = fields.Base64FileField
    serializer_field_mapping[models.ImageField] = fields.Base64ImageField
    serializer_field_mapping[models.CharField] = fields.AdminCharField
    serializer_field_mapping[models.TextField] = fields.AdminCharField

    serializer_field_mapping[models.PositiveIntegerField] = admin_fields.PositiveIntegerField
    serializer_field_mapping[custom_model_fields.PositiveDecimalField] = admin_fields.PositiveDecimalField


class AdminSerializer(AdminFieldsMixin, serializers.Serializer):
    pass


class AdminModelSerializer(AdminFieldsMixin, serializers.ModelSerializer):

    def create(self, validated_data):
        obj = super().create(validated_data)

        AdminLogManager(self.context['request'].user).register_create(self, validated_data, obj)
        return obj

    def update(self, instance, validated_data):
        data_before_update = {
            k: AdminLogManager.get_field_value(instance, k)
            for k, v in validated_data.items()
        }
        obj = super().update(instance, validated_data)

        AdminLogManager(self.context['request'].user).register_update(self, data_before_update, validated_data, obj)
        return obj


class TranslatedModelSerializer(AdminModelSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trans_opts = translator.get_options_for_model(self.Meta.model)

    def get_field_names(self, declared_fields, info):
        result = super().get_field_names(declared_fields, info)
        for f in self.trans_opts.fields:
            trans_fields = get_translation_fields(f)
            result += tuple(trans_fields)

        return result

    def get_extra_kwargs(self):
        extra_kwargs = super().get_extra_kwargs()
        for field in self.trans_opts.fields:

            if field not in extra_kwargs:
                extra_kwargs[field] = {}

            extra_kwargs[field]['required'] = False
            extra_kwargs[field]['allow_null'] = True
            extra_kwargs[field]['allow_blank'] = True

            if field in extra_kwargs:
                for tanslated_field in get_translation_fields(field):
                    extra_kwargs[tanslated_field] = extra_kwargs.get(field)

        return extra_kwargs


class OrderedAdminModelSerializer(AdminModelSerializer):
    """
    Класс для моделей с приоритетом OrderedModel

    если поле в моделе отличается от order, в сериализаторе надо его указать в order_field
    """
    order_field = 'order'

    def get_order_field(self):
        model_class = self.Meta.model
        order_field_name = getattr(model_class, "order_field_name", self.order_field)

        if not order_field_name:
            raise AttributeError(
                "The `order_field_name` attribute must be set to use the "
                "OrderedModelSerializer. Either inherit from OrderedModel "
                "(to use the default `order` field) or inherit from "
                "`OrderedModelBase` and set the `order_field_name` attribute "
                "on the " + model_class.__name__ + " Model class."
            )

        return order_field_name

    def get_fields(self):
        # make sure that DRF considers the ordering field writable
        order_field = self.get_order_field()
        d = super().get_fields()
        for name, field in d.items():
            if name == order_field:
                if field.read_only:
                    d[name] = fields.IntegerField()
        return d

    def update(self, instance, validated_data):
        """
        Update the instance.
        If the `order_field_name` attribute is passed in the validated data,
        the instance will be moved to the specified order.
        Returns:
            Model: The updated instance.
        """

        order = None
        order_field = self.get_order_field()

        if order_field in validated_data:
            order = validated_data.pop(order_field)

        instance = super().update(instance, validated_data)

        if order is not None:
            instance.to(order)

        return instance

    def create(self, validated_data):
        """
        Create a new instance.
        If the `order_field_name` attribute is passed in the validated data,
        the instance will be created at the specified order.
        Returns:
            Model: The created instance.
        """
        order = None
        order_field = self.get_order_field()

        if order_field in validated_data:
            order = validated_data.pop(order_field)

        instance = super().create(validated_data)

        if order is not None:
            instance.to(order)

        return instance
