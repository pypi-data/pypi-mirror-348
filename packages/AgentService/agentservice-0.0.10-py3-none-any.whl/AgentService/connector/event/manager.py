
import asyncio
from loguru import logger

from .event import BaseEvent

from typing import Callable
from AgentService.utils.singleton import SingletonMeta


class EventManager(metaclass=SingletonMeta):
    def __init__(self):
        self.log = logger.bind(classname=self.__class__.__name__)
        self.__callbacks: dict[BaseEvent, list[Callable]] = {sub: [] for sub in BaseEvent.__subclasses__()}
        self.__filters: dict[Callable, dict] = {}

    def bind(self, event: BaseEvent, callback: Callable, **kwargs):
        event_callbacks = self.__callbacks[event]
        if callback in event_callbacks:
            self.log.warning(f"Event {event} already binded on {callback}")
            return

        self.log.debug(f"Event {event} binded on {callback} with kwargs {kwargs}")
        event_callbacks.append(callback)
        self.__filters.update({callback: kwargs})

    def unbind(self, event: BaseEvent, callback: Callable):
        event_callbacks = self.__callbacks[event]
        if callback not in event_callbacks:
            self.log.warning(f"Event {event} already unbinded on {callback}")
            return

        self.log.debug(f"Event {event} unbinded on {callback}")
        event_callbacks.remove(callback)
        del self.__filters[callback]

    async def wrapper(self, func: Callable, event: BaseEvent):
        try:
            kwargs = self.__filters[func]
            for key in kwargs:
                value = event.__getattribute__(key)
                if value != kwargs[key]:
                    return

            await func(event=event)

        except Exception as err:
            self.log.exception(err)

    async def dispatch(self, event: BaseEvent):
        self.log.debug(f"Dispatching event {event}")
        event_callbacks = self.__callbacks[event.__class__]
        await asyncio.gather(*[
            self.wrapper(func=callback, event=event)
            for callback in event_callbacks
        ])
