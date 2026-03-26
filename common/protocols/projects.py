from uuid import UUID

from pydantic import BaseModel

from common.lib.rpc import rpc

__all__ = [
    "ProjectsProtocol",
    "ProjectGetResponse",
    "ProjectListRequest",
    "ProjectListResponse",
    "ProjectUpdateRequest",
    "ProjectUpdateResponse",
]


class BaseRequest(BaseModel):
    correlation_id: UUID | None = None


class ProjectGetResponse(BaseModel):
    id: UUID
    name: str
    description: str
    secret: str


class ProjectListRequest(BaseRequest):
    count: int


class ProjectListResponse(BaseModel):
    projects: list[ProjectGetResponse]


class ProjectUpdateRequest(BaseModel):
    id: UUID
    name: str
    description: str


class ProjectUpdateResponse(ProjectGetResponse): ...


class ProjectsProtocol:
    @rpc("projects.list")
    async def get_projects(
        self,
        message: ProjectListRequest,
    ) -> ProjectListResponse: ...

    @rpc("projects.update")
    async def update_project(
        self, message: ProjectUpdateRequest
    ) -> ProjectUpdateResponse: ...
