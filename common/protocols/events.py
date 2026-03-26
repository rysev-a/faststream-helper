from uuid import UUID

from pydantic import BaseModel

from common.lib.rpc import rpc

__all__ = [
    "EventsProtocol",
    "PublishEventRequest",
]


class BaseRequest(BaseModel):
    correlation_id: UUID | None = None


class PublishEventRequest(BaseModel):
    message: str


class EventsProtocol:
    @rpc("events.publish", call_type="publish")
    async def publish_event(
        self,
        message: PublishEventRequest,
    ) -> None: ...
