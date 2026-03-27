import uuid

import pytest
import pytest_asyncio
from common.lib.rpc import create_client
from common.protocols import ProjectListRequest
from common.protocols import ProjectsProtocol
from services.projects_service.app.main import app as projects_app
from services.secrets_service.app.main import app as secret_app


@pytest_asyncio.fixture
async def service_app():
    await projects_app.start()
    await secret_app.start()
    yield
    await projects_app.stop()
    await secret_app.stop()


@pytest.mark.asyncio
async def test_projects_rpc_service(service_app):
    projects_client = create_client(ProjectsProtocol)(uuid.uuid4())
    response = await projects_client.get_projects(ProjectListRequest(count=1))
    assert len(response.projects) == 1
    assert response.projects[0].name == "name 0"
