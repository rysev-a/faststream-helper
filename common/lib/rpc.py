import dataclasses
import functools
import inspect
from abc import ABC
from contextlib import asynccontextmanager
from types import MethodType
from typing import TypeVar
from uuid import UUID

from faststream import FastStream
from faststream.nats import NatsRoute, NatsRouter

from .broker import nats_broker


class ProtocolNotFoundError(Exception): ...


T = TypeVar("T")


@dataclasses.dataclass
class RpcMethod:
    subject: str
    method_name: str
    method_func: MethodType
    call_type: str


@dataclasses.dataclass
class RpcMeta:
    subject: str
    call_type: str


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


def create_service(resolver_classes: list[type[RpcService]]) -> FastStream:
    services = []

    for resolver_class in resolver_classes:
        resolver = resolver_class()
        services.append(resolver)

        contract_class = None

        for base_class in resolver_class.__bases__:
            if base_class.__name__.endswith("Protocol"):
                contract_class = base_class

        if contract_class is None:
            raise ProtocolNotFoundError(f"protocol not found for {resolver_class}")

        router = NatsRouter(
            handlers=(
                NatsRoute(getattr(resolver, rpc_method.method_name), rpc_method.subject)
                for rpc_method in _get_rpc_methods(contract_class)
            ),
        )
        nats_broker.include_router(router)

    @asynccontextmanager
    async def lifespan():
        for service in services:
            await service.start()
        yield
        for service in services:
            await service.stop()

    return FastStream(nats_broker, lifespan=lifespan)


def create_client(contract_class: T) -> type[T]:
    def init(self, correlation_id: UUID):
        self.correlation_id = correlation_id

    setattr(contract_class, "__init__", init)

    def __handle_rpc_call(
        message_subject: str, call_type: str, method_function: MethodType
    ):
        async def func(self, message):
            if call_type == "request":
                response = await nats_broker.request(
                    message,
                    subject=message_subject,
                    timeout=30,
                    correlation_id=str(self.correlation_id),
                )
                return_type = inspect.getfullargspec(method_function).annotations.get(
                    "return"
                )
                return return_type.model_validate_json(response.body.decode("utf-8"))
            if call_type == "publish":
                await nats_broker.publish(
                    message,
                    subject=message_subject,
                    timeout=30,
                    correlation_id=str(self.correlation_id),
                )
            return None

        return func

    for rpc_method in _get_rpc_methods(contract_class):
        setattr(
            contract_class,
            rpc_method.method_name,
            __handle_rpc_call(
                rpc_method.subject, rpc_method.call_type, rpc_method.method_func
            ),
        )
    return contract_class


def _get_rpc_methods(
    contract_class,
) -> list[RpcMethod]:
    rpc_methods = []
    for method_name in dir(contract_class):
        method_func: MethodType = getattr(contract_class, method_name)
        if callable(method_func):
            if hasattr(method_func, "rpc"):
                rpc_meta = getattr(method_func, "rpc")
                rpc_methods.append(
                    RpcMethod(
                        subject=rpc_meta.subject,
                        method_name=method_name,
                        method_func=method_func,
                        call_type=rpc_meta.call_type,
                    )
                )
    return rpc_methods


def rpc(subject: str, call_type="request"):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)

        wrapper.rpc = RpcMeta(subject=subject, call_type=call_type)
        return wrapper

    return decorator
