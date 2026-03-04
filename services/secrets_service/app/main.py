from common.lib.rpc import create_service
from common.protocols import SecretsProtocol

from .service import SecretsService

app = create_service(SecretsService, SecretsProtocol)
