
from typing import Callable

from .manager import EventManager
from .event import BaseEvent


async def dispatch_event(event: BaseEvent):
    manager = EventManager()
    return await manager.dispatch(event)


def bind_event(event: BaseEvent, callback: Callable, **kwargs):
    manager = EventManager()
    manager.bind(event, callback, **kwargs)


def unbind_event(event: BaseEvent, callback: Callable, **kwargs):
    manager = EventManager()
    manager.unbind(event, callback, **kwargs)
