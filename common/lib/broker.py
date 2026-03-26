import os

from faststream.nats import NatsBroker

print(os.environ["NATS_URL"])
nats_broker = NatsBroker(servers=(os.environ["NATS_URL"],), connect_timeout=1)
