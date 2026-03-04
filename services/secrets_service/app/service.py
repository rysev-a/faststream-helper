from common.lib.rpc import RpcService
from common.protocols import (
    GetSecretRequest,
    GetSecretResponse,
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
