import uuid

from faststream import Depends, Logger

from common.contracts.projects_service import (
    ProjectGetResponse,
    ProjectListRequest,
    ProjectListResponse,
    ProjectsContracts,
)
from common.lib.rpc import ServiceResolver

value = {"count": 0}


def simple_dependency() -> int:
    return value["count"]


class ProjectService(ServiceResolver, ProjectsContracts):
    def __init__(self):
        self.info = "project service"

    async def start(self):
        print("run project service")

    async def get_projects(
        self,
        message: ProjectListRequest,
        d: int = Depends(simple_dependency),
        logger: Logger = None,
    ) -> ProjectListResponse:
        value["count"] += 1
        logger.info(d)

        return ProjectListResponse(
            projects=[
                ProjectGetResponse(
                    id=uuid.uuid4(),
                    name=f"name {i}",
                    description=f"description {d}",
                )
                for i in range(message.count)
            ]
        )

    async def stop(self):
        print("stop")
