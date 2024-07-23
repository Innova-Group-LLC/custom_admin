import asyncio as aio
import functools
import typing

from asgiref.sync import sync_to_async

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

        # elevated, flat, tonal, outlined, text, and plain.
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
        func.variant = variant
        func.base_color = base_color
        func.allow_empty_selection = allow_empty_selection

        if form_serializer:
            from custom_admin.api.serializers import AdminSerializer
            if not issubclass(form_serializer, AdminSerializer):
                raise Exception(f'{func.__name__}.form_serializer must be instance of AdminSerializer')
            func.form_serializer = form_serializer

        @functools.wraps(func)
        async def wrapper(*args, **kwargs):

            f = func
            if not aio.iscoroutinefunction(func):
                f = sync_to_async(func)
            return await f(*args, **kwargs)

        return wrapper
    return decorator
