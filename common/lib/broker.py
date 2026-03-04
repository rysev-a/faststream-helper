import os

from faststream.nats import NatsBroker

nats_broker = NatsBroker(servers=(os.environ["NATS_URL"],), connect_timeout=1)
