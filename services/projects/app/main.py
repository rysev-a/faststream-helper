import os

from faststream.nats import NatsBroker, NatsMessage

from common.contracts.project import ProjectContracts
from common.lib.rpc import create_service

from .service import ProjectService

broker = NatsBroker(os.environ["NATS_URL"])
app = create_service(ProjectService, ProjectContracts, broker)
