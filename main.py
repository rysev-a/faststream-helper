from contextlib import asynccontextmanager

from fastapi import FastAPI
from faststream.nats import NatsBroker

from contracts.project import ProjectContracts, ProjectListRequest, ProjectListResponse
from rpc import create_client

broker = NatsBroker()
project_client = create_client(ProjectContracts, broker)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await broker.start()
    yield
    await broker.stop()


app = FastAPI(lifespan=lifespan)


@app.get("/projects/{count}")
async def root(count: int):
    return await project_client.get_projects(ProjectListRequest(count=count))
