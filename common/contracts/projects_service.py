from uuid import UUID

from pydantic import BaseModel

from ..lib.rpc import subject


class BaseRequest(BaseModel):
    correlation_id: UUID | None = None


class ProjectGetResponse(BaseModel):
    id: UUID
    name: str
    description: str


class ProjectListRequest(BaseRequest):
    count: int


class ProjectListResponse(BaseModel):
    projects: list[ProjectGetResponse]


class ProjectUpdateRequest(BaseModel):
    id: UUID
    name: str
    description: str


class ProjectUpdateResponse(ProjectGetResponse): ...


class ProjectsContracts:
    @subject("projects.list")
    async def get_projects(
        self,
        message: ProjectListRequest,
    ) -> ProjectListResponse: ...

    @subject("projects.update")
    async def update_project(
        self, message: ProjectUpdateRequest
    ) -> ProjectUpdateResponse: ...
