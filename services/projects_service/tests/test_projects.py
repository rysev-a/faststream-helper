from common.lib.rpc import create_client
from common.protocols import ProjectsProtocol

projects_client = create_client(ProjectsProtocol)


async def test_something():
    assert True
