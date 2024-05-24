import functools
import typing

ACTION_ATTRIBUTES = [
    'description',
    'short_description',
    'confirmation_text',
    'icon',
    'variant',
    'base_color',
    'allow_empty_selection',
]

def admin_action(
        description: typing.Optional[str] = None,
        short_description: typing.Optional[str] = None,
        confirmation_text: typing.Optional[str] = None,

        # https://pictogrammers.com/library/mdi/
        icon: typing.Optional[str] = None,
        variant: typing.Optional[str] = None,
        base_color: typing.Optional[str] = None,

        allow_empty_selection: bool = False,

        form_serializer=None,
):
    def decorator(func):
        func.description = description
        func.short_description = short_description
        func.confirmation_text = confirmation_text
        func.icon = icon
        func.base_color = base_color
        func.allow_empty_selection = allow_empty_selection

        if form_serializer:
            from custom_admin.api.serializers import AdminSerializer
            if not issubclass(form_serializer, AdminSerializer):
                raise Exception(f'{func.__name__}.form_serializer must be instance of AdminSerializer')
            func.form_serializer = form_serializer

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator
