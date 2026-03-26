from faststream import Logger

from common.lib.rpc import RpcService
from common.protocols import (
    EventsProtocol,
    GetSecretRequest,
    GetSecretResponse,
    PublishEventRequest,
    PutSecretRequest,
    PutSecretResponse,
    SecretsProtocol,
)


class SecretsService(RpcService, SecretsProtocol):
    async def start(self): ...

    async def get_secret(self, message: GetSecretRequest) -> GetSecretResponse:
        return GetSecretResponse(data=f"secret for {message.id}")

    async def put_secret(self, message: PutSecretRequest) -> PutSecretResponse:
        return PutSecretResponse(id=message.id)


class EventService(RpcService, EventsProtocol):
    async def start(self): ...

    async def stop(self): ...

    async def publish_event(
        self,
        message: PublishEventRequest,
        logger: Logger = None,
    ) -> None:
        logger.info("publishing event from secrets")
