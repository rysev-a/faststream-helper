from common.lib.rpc import create_service

from .service import ProjectService, EventService

app = create_service([ProjectService, EventService])
