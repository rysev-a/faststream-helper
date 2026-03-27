from uuid import uuid4

from faststream import Depends, Logger

from common.lib.dependencies import provide_rpc_client
from common.lib.rpc import RpcService
from common.protocols import (
    EventsProtocol,
    GetSecretRequest,
    ProjectGetResponse,
    ProjectListRequest,
    ProjectListResponse,
    ProjectsProtocol,
    PublishEventRequest,
    SecretsProtocol,
)


class EventService(RpcService, EventsProtocol):
    async def start(self): ...

    async def stop(self): ...

    async def publish_event(
        self,
        message: PublishEventRequest,
        logger: Logger = None,
    ):
        logger.info("publish event from projects")


class ProjectService(RpcService, ProjectsProtocol):
    def __init__(self):
        self.info = "project service"

    async def start(self):
        print("run project service")

    async def get_projects(
        self,
        message: ProjectListRequest,
        secrets_client: SecretsProtocol = Depends(provide_rpc_client(SecretsProtocol)),
        events_client: EventsProtocol = Depends(provide_rpc_client(EventsProtocol)),
        logger: Logger = None,
    ) -> ProjectListResponse:
        logger.info("get projects list")

        projects: list[ProjectGetResponse] = []
        for i in range(message.count):
            project_id = uuid4()
            projects.append(
                ProjectGetResponse(
                    id=project_id,
                    name=f"name {i}",
                    description=f"description {i}",
                    secret=(
                        await secrets_client.get_secret(GetSecretRequest(id=project_id))
                    ).data,
                )
            )

        # await events_client.publish_event(
        #     PublishEventRequest(message="get projects success")
        # )

        return ProjectListResponse(
            projects=projects,
        )

    async def stop(self):
        print("stop")
