import dataclasses
import functools
import inspect
from abc import ABC
from contextlib import asynccontextmanager
from types import MethodType
from typing import TypeVar
from uuid import UUID

from faststream import FastStream
from faststream.nats import NatsBroker, NatsRoute, NatsRouter

from .broker import nats_broker

T = TypeVar("T")


@dataclasses.dataclass
class RpcMethod:
    subject: str
    method_name: str
    method_func: MethodType


class RpcService(ABC):
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


def create_service(resolver_class: type[RpcService], contract_class) -> FastStream:
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
    nats_broker.include_router(router)
    return FastStream(nats_broker, lifespan=lifespan)


def create_client(contract_class: T, broker: NatsBroker) -> T:
    def init(self, correlation_id: UUID):
        self.correlation_id = correlation_id

    setattr(contract_class, "__init__", init)

    def __handle_rpc_call(message_subject: str, method_function: MethodType):
        async def func(self, message):
            response = await broker.request(
                message,
                subject=message_subject,
                timeout=30,
                correlation_id=str(self.correlation_id),
            )
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
        method_func: MethodType = getattr(contract_class, method_name)
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


def subject(subject_name: str):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)

        wrapper.subject = subject_name
        return wrapper

    return decorator
