import uuid
from typing import Generator

from fastapi import Depends, Request
from faststream import Context
from faststream.nats import NatsBroker

from common.lib.rpc import create_client

from .broker import nats_broker


def provide_broker() -> NatsBroker:
    return nats_broker


def provide_correlation_id(request: Request) -> uuid.UUID:
    correlation_id = request.headers.get("correlation-id")
    if correlation_id is None:
        return uuid.uuid4()
    return uuid.UUID(correlation_id)


def provider_client[T](service_contracts: T):
    def provide(
        correlation_id: uuid.UUID = Depends(provide_correlation_id),
    ) -> Generator[T]:
        yield create_client(service_contracts)(correlation_id)

    return provide


def provide_rpc_client[T](protocol: T):
    def provide(
        correlation_id: str = Context("message.correlation_id"),
    ) -> T:
        yield create_client(protocol)(uuid.UUID(correlation_id))

    return provide
