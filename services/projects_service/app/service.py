from uuid import UUID, uuid4

from faststream import Context, Depends, Logger
from faststream.nats import NatsBroker

from common.lib.dependencies import provider_rpc_client
from common.lib.rpc import RpcService
from common.protocols import (
    GetSecretRequest,
    ProjectGetResponse,
    ProjectListRequest,
    ProjectListResponse,
    ProjectsProtocol,
    SecretsProtocol,
)


class ProjectService(RpcService, ProjectsProtocol):
    def __init__(self):
        self.info = "project service"

    async def start(self):
        print("run project service")

    async def get_projects(
        self,
        message: ProjectListRequest,
        secrets_client: SecretsProtocol = Depends(provide_rpc_client(SecretsProtocol)),
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

        return ProjectListResponse(projects=projects)

    async def stop(self):
        print("stop")
