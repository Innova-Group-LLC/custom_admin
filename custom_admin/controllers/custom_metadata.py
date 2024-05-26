from collections import OrderedDict

from django.utils.encoding import force_str
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.metadata import SimpleMetadata

from custom_admin.api import fields


class CustomMetadata(SimpleMetadata):

    def get_field_info(self, field):
        """
        Given an instance of a serializer field, return a dictionary
        of metadata about it.
        """
        field_info = OrderedDict()
        field_info['type'] = self.label_lookup[field]
        field_info['required'] = getattr(field, 'required', False)
        field_info['help_text'] = False

        attrs = [
            'read_only', 'label', 'help_text',
            'min_length', 'max_length',
            'min_value', 'max_value', 'write_only', 'max_width', 'initial',
            'wysiwyg', 'multilined', 'tag_style', 'json_forms', 'list_preview',
        ]

        for attr in attrs:
            value = getattr(field, attr, None)
            if value is not None and value != '':
                field_info[attr] = value
                if not isinstance(value, (dict, list)):
                    field_info[attr] = force_str(value, strings_only=True)

        if getattr(field, 'child', None):
            field_info['child'] = self.get_field_info(field.child)
        elif getattr(field, 'fields', None):
            field_info['children'] = self.get_serializer_info(field)

        is_inst = isinstance(field, (serializers.RelatedField, serializers.ManyRelatedField))
        field_info['update_only'] = getattr(field, 'update_only', False)

        field_info['create_only'] = getattr(field, 'create_only', False)
        field_info['list_only'] = getattr(field, 'list_only', False)
        if hasattr(field, 'initial'):
            field_info['initial'] = field.initial

        if hasattr(field, 'child_relation'):
            if hasattr(field.child_relation, 'update_only'):
                field_info['update_only'] = field.child_relation.update_only
            if hasattr(field.child_relation, 'create_only'):
                field_info['create_only'] = field.child_relation.create_only

        if (not field_info.get('read_only') and not is_inst and hasattr(field, 'choices')):
            field_info['choices'] = [
                {
                    'value': choice_value,
                    'display_name': str(_(choice_name))
                }
                for choice_value, choice_name in field.choices.items()
            ]

        elif issubclass(field.__class__, (serializers.PrimaryKeyRelatedField, fields.AdminPrimaryKeyRelatedField)):
            field_info['type'] = 'primary'

            if hasattr(field, 'queryset') and field.queryset is not None:
                field_info['model_name'] = field.queryset.model.__name__
                field_info['app_label'] = field.queryset.model._meta.app_label

        elif issubclass(field.__class__, (serializers.ManyRelatedField,)):
            field_info['type'] = 'primarymany'

            if field.child_relation and field.child_relation.queryset is not None:
                field_info['model_name'] = field.child_relation.queryset.model.__name__
                field_info['app_label'] = field.child_relation.queryset.model._meta.app_label

        elif issubclass(field.__class__, (fields.Base64ImageField,)):
            field_info['type'] = 'image upload'

        elif issubclass(field.__class__, (fields.SVGField,)):
            field_info['type'] = 'svgfield'

        elif issubclass(field.__class__, (serializers.JSONField,)):
            field_info['type'] = 'json'

        filter_queryset = getattr(field, 'filter_queryset', False)
        if filter_queryset:
            field_info['filter_queryset'] = filter_queryset.__name__

        return field_info
