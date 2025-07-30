from typing import Any

import pytest

from lihil import Route, status, Annotated, Param
from lihil.plugins.bus import Event, EventBus
from lihil.plugins.testclient import LocalClient


class TodoCreated(Event):
    name: str
    content: str


async def listen_create(created: TodoCreated, _: Any, bus: EventBus):
    assert created.name
    assert created.content
    assert isinstance(bus, EventBus)


async def listen_twice(created: TodoCreated, _: Any):
    assert created.name
    assert created.content


@pytest.fixture
async def bus_route():
    route = Route("/bus", listeners=[listen_create, listen_twice])
    await route.setup()
    return route


async def test_bus_is_singleton(bus_route: Route):
    async def create_todo(
        name: str, content: str, bus: Annotated[EventBus, Param("plugin")]
    ) -> Annotated[None, status.OK]:
        await bus.publish(TodoCreated(name, content))

    bus_route.post(create_todo)

    ep = bus_route.get_endpoint("POST")
    await bus_route.setup()
    assert ep.sig.plugins
    assert any(p.type_ is EventBus for p in ep.sig.plugins.values())


async def test_call_ep_invoke_bus(bus_route: Route):
    async def create_todo(
        name: str, content: str, bus: EventBus
    ) -> Annotated[None, status.OK]:
        await bus.publish(TodoCreated(name, content))

    bus_route.post(create_todo)
    ep = bus_route.get_endpoint("POST")
    client = LocalClient()
    await client.call_endpoint(ep, query_params=dict(name="1", content="2"))
