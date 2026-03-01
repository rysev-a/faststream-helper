import dataclasses
import inspect
from abc import ABC
from contextlib import asynccontextmanager
from types import FunctionType
from typing import TypeVar

from faststream import FastStream
from faststream.nats import NatsBroker, NatsRoute, NatsRouter

T = TypeVar("T")


@dataclasses.dataclass
class RpcMethod:
    subject: str
    method_name: str
    method_func: FunctionType


class ServiceResolver(ABC):
    async def start(self):
        """
        Create database connections, init cache etc.
        """
        raise NotImplementedError()

    async def stop(self):
        """
        Close database connections, clear cache etc.
        """
        raise NotImplementedError()


def create_service(resolver_class: type[ServiceResolver], contract_class) -> FastStream:
    broker = NatsBroker("nats://localhost:4222")
    resolver = resolver_class()

    @asynccontextmanager
    async def lifespan():
        await resolver.start()
        yield
        await resolver.stop()

    router = NatsRouter(
        handlers=(
            NatsRoute(getattr(resolver, rpc_method.method_name), rpc_method.subject)
            for rpc_method in _get_rpc_methods(contract_class)
        ),
    )
    broker.include_router(router)
    return FastStream(broker, lifespan=lifespan)


def create_client(contract_class: T, broker) -> T:
    def __handle_rpc_call(subject: str, method_function: FunctionType):
        async def func(message):
            response = await broker.request(message, subject=subject, timeout=30)
            return_type = inspect.getfullargspec(method_function).annotations.get(
                "return"
            )
            return return_type.model_validate_json(response.body.decode("utf-8"))

        return func

    for rpc_method in _get_rpc_methods(contract_class):
        setattr(
            contract_class,
            rpc_method.method_name,
            __handle_rpc_call(rpc_method.subject, rpc_method.method_func),
        )
    return contract_class


def _get_rpc_methods(
    contract_class,
) -> list[RpcMethod]:
    rpc_methods = []
    for method_name in dir(contract_class):
        method_func = getattr(contract_class, method_name)
        if callable(method_func):
            if hasattr(method_func, "subject"):
                subject = getattr(method_func, "subject")
                rpc_methods.append(
                    RpcMethod(
                        subject=subject,
                        method_name=method_name,
                        method_func=method_func,
                    )
                )
    return rpc_methods
