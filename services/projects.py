import uuid

from faststream import Depends

from contracts.project import (
    ProjectContracts,
    ProjectGetResponse,
    ProjectListRequest,
    ProjectListResponse,
)
from rpc import ServiceResolver, create_service

value = {"count": 0}


def simple_dependency():
    return value["count"]


class ProjectService(ServiceResolver, ProjectContracts):
    def __init__(self):
        self.info = "project service"

    async def start(self):
        print("start")

    async def get_projects(
        self, message: ProjectListRequest, d: int = Depends(simple_dependency)
    ) -> ProjectListResponse:
        value["count"] += 1
        print(d)
        return ProjectListResponse(
            projects=[
                ProjectGetResponse(
                    id=uuid.uuid4(),
                    name=f"name {i} {d}",
                    description=f"description {i}",
                )
                for i in range(message.count)
            ]
        )

    async def handle(self, body):
        return f"Hi {body} {self.info} ok"

    async def handle_test(self, body):
        return f"Hi {body} {self.info} ok test"

    async def stop(self):
        print("stop")


app = create_service(ProjectService, ProjectContracts)
