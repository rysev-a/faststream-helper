import functools
from abc import ABC
from uuid import UUID

from pydantic import BaseModel


def rpc(subject: str):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)

        wrapper.subject = subject
        return wrapper

    return decorator


class ProjectGetResponse(BaseModel):
    id: UUID
    name: str
    description: str


class ProjectListRequest(BaseModel):
    count: int


class ProjectListResponse(BaseModel):
    projects: list[ProjectGetResponse]


class ProjectUpdateRequest(BaseModel):
    id: UUID
    name: str
    description: str


class ProjectUpdateResponse(ProjectGetResponse): ...


class ProjectContracts:
    @rpc("projects.list")
    async def get_projects(
        self, message: ProjectListRequest
    ) -> ProjectListResponse: ...

    @rpc("projects.update")
    async def update_project(
        self, project: ProjectUpdateRequest
    ) -> ProjectUpdateResponse: ...
