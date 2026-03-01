from faststream import Depends, FastStream
from faststream.nats import NatsBroker

broker = NatsBroker()

app = FastStream(broker)

value = {"count": 0}


def simple_dependency():
    return value["count"]


@broker.subscriber(subject="users.list")
async def list_users(message, d: int = Depends(simple_dependency)):
    value["count"] += 1
    return {"users": f"{message} - {d}"}
