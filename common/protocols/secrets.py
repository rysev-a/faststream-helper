from uuid import UUID

from pydantic import BaseModel

from common.lib.rpc import rpc


class GetSecretRequest(BaseModel):
    id: UUID


class GetSecretResponse(BaseModel):
    data: str


class PutSecretRequest(BaseModel):
    id: UUID
    data: str


class PutSecretResponse(BaseModel):
    id: UUID


class SecretsProtocol:
    @rpc("secrets.get")
    async def get_secret(self, message: GetSecretRequest) -> GetSecretResponse: ...

    @rpc("secrets.put")
    async def put_secret(self, message: PutSecretRequest) -> GetSecretResponse: ...
