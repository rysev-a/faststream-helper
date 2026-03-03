import os
import uuid
from contextlib import asynccontextmanager
from typing import Annotated, Generator, TypeAlias

from fastapi import Depends, FastAPI, Request
from faststream.nats import NatsBroker

from common.contracts.projects_service import (
    ProjectListRequest,
    ProjectsContracts,
)
from common.lib.rpc import create_client

broker = NatsBroker(servers=(os.environ["NATS_URL"],), connect_timeout=1)


def provide_correlation_id(request: Request) -> uuid.UUID:
    correlation_id = request.headers.get("correlation-id")
    if correlation_id is None:
        return uuid.uuid4()
    return uuid.UUID(correlation_id)


def provider_client[T](service_contracts: T):
    def provide(
        correlation_id: uuid.UUID = Depends(provide_correlation_id),
    ) -> Generator[T]:
        yield create_client(service_contracts, broker)(correlation_id)

    return provide


ProjectsClientDependency: TypeAlias = Annotated[
    ProjectsContracts, Depends(provider_client(ProjectsContracts))
]


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await broker.start()
    yield
    await broker.stop()


app = FastAPI(lifespan=lifespan)


@app.get("/api/projects/{count}")
async def root(
    count: int,
    project_client: ProjectsClientDependency,
):
    return await project_client.get_projects(ProjectListRequest(count=count))
