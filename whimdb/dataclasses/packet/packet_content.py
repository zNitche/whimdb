from typing import Any
from dataclasses import dataclass
from whimdb.dataclasses.mixins import SerializableObjectMixin
from whimdb.dataclasses.communication import Response, Request


@dataclass
class PacketContent(SerializableObjectMixin):
    # client consumable
    response: Response | None = None

    # server consumables
    request: Request | None = None

    def dump(self) -> dict[str, Any]:
        return {
            "response": self.response.to_dict() if self.response else None,
            "request": self.request.to_dict() if self.request else None
        }

    @staticmethod
    def loads(**kwargs):
        raw_response = kwargs.get("response")
        raw_request = kwargs.get("request")

        response = Response.from_dict(**raw_response) if raw_response else None
        request = Request.from_dict(**raw_request) if raw_request else None

        return PacketContent(
            response=response,
            request=request
        )
