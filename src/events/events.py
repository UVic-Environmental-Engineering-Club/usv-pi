""" Subscriber/Observer programming paradigm """

import asyncio
from typing import Any
from collections.abc import Callable
from src.constants import EVENT_LIST, SUBSCRIBERS
from src.events.event_type import EventType


def subscribe(
    event: EventType,
    func: Callable[[Any], Any],
) -> None:
    """Adds an EventType and observer function to subscribers"""
    if not event in SUBSCRIBERS:
        SUBSCRIBERS[event] = []
    SUBSCRIBERS[event].append(func)


async def post_event(event: EventType, data: Any = None) -> None:
    """Runs all observer functions for the EventType"""
    await EVENT_LIST.put((event, data))


async def run_event_loop() -> None:
    """Infinite loop for running event loop"""
    while True:
        await asyncio.sleep(0.01)
        if not EVENT_LIST.empty():
            [event_type, data] = await EVENT_LIST.get()

            coroutines = []
            for func in SUBSCRIBERS[event_type]:
                coroutines.append(asyncio.create_task(func(data) if data else func()))

            await asyncio.gather(*coroutines)
