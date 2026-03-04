from contextlib import asynccontextmanager
from typing import Annotated, TypeAlias

from fastapi import Depends, FastAPI

from common.lib.broker import nats_broker
from common.lib.dependencies import provider_client
from common.protocols import (
    ProjectListRequest,
    ProjectListResponse,
    ProjectsProtocol,
    SecretsProtocol,
)

ProjectsClientDependency: TypeAlias = Annotated[
    ProjectsProtocol, Depends(provider_client(ProjectsProtocol))
]


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await nats_broker.start()
    yield
    await nats_broker.stop()


app = FastAPI(lifespan=lifespan)


@app.get("/api/projects/")
async def root(
    project_client: ProjectsClientDependency,
) -> ProjectListResponse:
    return await project_client.get_projects(ProjectListRequest(count=5))
