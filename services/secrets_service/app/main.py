from common.lib.rpc import create_service

from .service import EventService, SecretsService

app = create_service([SecretsService, EventService])
