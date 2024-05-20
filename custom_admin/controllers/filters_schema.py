from django.utils.translation import gettext as _
from django_filters import filters
from django_filters.utils import get_model_field


class ModelFieldException(Exception):
    pass


def get_filters_fields_data(model, filters):
    result = {}
    for f in filters:
        filter_name = None
        filter_field = None

        if isinstance(f, str):
            filter_name = f
            filter_field = get_model_field(model, f)
            if not filter_field:
                raise ModelFieldException(f'Field "{f}" not found in {model.__name__}')

        elif isinstance(f, (list, tuple)):
            filter_name = f[0]
            filter_field = f[1]

        result[filter_name] = {'type': filter_field.__class__.__name__}

        if result[filter_name]['type'] == 'ManyToManyRel':
            result[filter_name]['label'] = str(_(filter_field.related_model._meta.verbose_name))
        else:
            result[filter_name]['label'] = str(_(filter_field.verbose_name))

        if result[filter_name]['type'] in ('ForeignKey', 'ManyToManyField', 'OneToOneField', 'ManyToManyRel'):
            result[filter_name]['model_name'] = filter_field.related_model.__name__
            result[filter_name]['app_label'] = filter_field.related_model._meta.app_label

        if hasattr(filter_field, 'choices') and filter_field.choices:
            choices = tuple({
                'value': c[0],
                'display_name': str(_(c[1]))
            } for c in filter_field.choices)
            if choices:
                result[filter_name]['choices'] = choices

    return result


def get_filters_class_data(model, filter_class, request) -> dict:
    result = {}

    for filter_name, filter_field in filter_class.get_filters().items():
        name = filter_field.label
        if not name:
            field = get_model_field(model, filter_field.field_name)
            if field:
                name = _(field.verbose_name)

        result[filter_name] = {
            'type': filter_field.__class__.__name__,
            'label': str(name),
        }

        filter_model = None

        if result[filter_name]['type'] in ('ModelChoiceFilter', 'OneToOneField', 'ModelMultipleChoiceFilter'):
            filter_model = filter_field.get_queryset(request).model

        elif result[filter_name]['type'] in ('ManyRelatedField', 'AdminManyRelatedField'):
            filter_model = filter_field.child_relation.queryset.model

        if filter_model:
            model_name = filter_model.__name__
            app_label = filter_model._meta.app_label
            result[filter_name]['model_name'] = model_name
            result[filter_name]['app_label'] = app_label

        if isinstance(filter_field, filters.Filter):
            choices = filter_field.extra.get('choices')
            if choices:
                choices = tuple({
                    'value': c[0],
                    'display_name': str(_(c[1]))
                } for c in choices)
                if choices:
                    result[filter_name]['choices'] = choices

    return result
