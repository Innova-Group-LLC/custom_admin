import functools
import typing


def admin_action(
        description: typing.Optional[str] = None,
        short_description: typing.Optional[str] = None,

        # https://element.eleme.io/#/en-US/component/icon
        icon: typing.Optional[str] = None,

        # https://element.eleme.io/#/en-US/component/button
        inline_type: typing.Optional[str] = None,
        inline_only: bool = False,

        form_serializer=None,
):
    def decorator(func):
        func.description = description
        func.short_description = short_description
        func.icon = icon
        func.inline_type = inline_type
        func.inline_only = inline_only

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
