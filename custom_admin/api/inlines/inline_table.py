import typing
from dataclasses import asdict, dataclass, field

from django.core.paginator import Paginator
from rest_framework import serializers

from custom_admin.api.inlines.interfaces import InlineResultInterface
from custom_admin.api.inlines.view_inline_mixin import InlineError


@dataclass
class ColumnInfo:
    width: typing.Optional[int] = None
    fixed: bool = False
    html: bool = False


@InlineResultInterface.register
@dataclass
class InlineTableResult:
    columns_info: typing.Dict[str, ColumnInfo] = field(default_factory=dict)

    messages: typing.List[dict] = field(default_factory=dict)
    paginator: typing.Optional[Paginator] = None

    serializer: typing.Optional[serializers.Serializer] = None

    # Depricated!
    columns: typing.List[str] = field(default_factory=list)
    # Depricated!
    data: typing.List[list] = field(default_factory=list)

    def set_up_serializer(self):
        if not self.serializer:
            return

        self.columns = []

        if hasattr(self.serializer, 'child'):
            self.data = [d.values() for d in self.serializer.data]
            for field_key, field_value in self.serializer.child.get_fields().items():
                self.columns.append(field_value.label)
        else:
            raise InlineError(f'{self.serializer.__class__} is not implemented for InlineTableResult')

    def __post_init__(self):
        self.set_up_serializer()

    def asdict(self) -> dict:
        result = {}

        formated_data = []
        if self.data:
            for line in self.data:
                formated_data.append({
                    str(self.columns[i]): item
                    for i, item in enumerate(line)
                })
            result['data'] = formated_data

        result['columns'] = self.columns
        result['messages'] = self.messages

        result['columns_info'] = {
            k: asdict(v)
            for k, v in self.columns_info.items()
        }

        if self.paginator:
            result['count'] = self.paginator.count
            result['num_pages'] = self.paginator.num_pages

        return result
