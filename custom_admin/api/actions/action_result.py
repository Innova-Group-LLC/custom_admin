import typing
from dataclasses import dataclass

from rest_framework.response import Response


@dataclass
class ActionResult:
    status_code: int = 200
    messages: typing.Optional[typing.List[str]] = None

    persistent_message: typing.Optional[str] = None

    def to_response(self) -> Response:
        data = {
            'action_messages': self.messages,
            'persistent_message': self.persistent_message,
        }
        return Response(data, status=self.status_code)
