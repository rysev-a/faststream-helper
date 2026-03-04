from common.lib.rpc import create_service
from common.protocols import ProjectsProtocol

from .service import ProjectService

app = create_service(ProjectService, ProjectsProtocol)
