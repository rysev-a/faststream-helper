import os

from faststream.nats import NatsBroker, NatsMessage

from common.contracts.projects_service import ProjectsContracts
from common.lib.rpc import create_service

from .service import ProjectService

broker = NatsBroker(os.environ["NATS_URL"])
app = create_service(ProjectService, ProjectsContracts, broker)
