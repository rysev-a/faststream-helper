import uuid
from collections.abc import Callable

from faststream import Context, Depends, Logger
from faststream.nats import NatsMessage

from common.contracts.project import (
    ProjectContracts,
    ProjectGetResponse,
    ProjectListRequest,
    ProjectListResponse,
)
from common.lib.rpc import ServiceResolver

value = {"count": 0}


def simple_dependency() -> int:
    return value["count"]


class ProjectService(ServiceResolver, ProjectContracts):
    def __init__(self):
        self.info = "project service"

    async def start(self):
        print("run project service")

    async def get_projects(
        self,
        message: ProjectListRequest,
        logger: Logger,
        d: int = Depends(simple_dependency),
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
