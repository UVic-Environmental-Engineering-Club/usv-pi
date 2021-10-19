""" Subscriber/Observer programming paradigm """

import functools
from multiprocessing import Manager, Pool
from multiprocessing.context import Process
from typing import Dict, List, Any, Tuple
from collections.abc import Callable
from src.events.event_type import EventType


def subscribe(
    manager: Manager,
    subscribers: Dict[EventType, List[Callable[[Any], Any]]],
    event: EventType,
    func: Callable[[Any], Any],
) -> None:
    """Adds an EventType and observer function to subscribers"""
    if not event in subscribers:
        subscribers[event] = manager.list()
    subscribers[event].append(func)


def post_event(
    event_list: List[Tuple[EventType, Any]], event: EventType, data: Any
) -> None:
    """Runs all observer functions for the EventType"""
    event_list.append((event, data))
    print(event_list)


def smap(func) -> Callable[[Any], Any]:
    """Helper function that returns function thats passed in"""
    return func()


def run_event_loop(
    subscribers: Dict[EventType, List[Callable[[Any], Any]]],
    event_list: List[Tuple[EventType, Any]],
) -> None:
    """Infinite loop for running event loop"""
    while True:
        if len(event_list) != 0:
            functions: List[Process] = []

            [event_type, data] = event_list.pop()
            for func in subscribers[event_type]:
                functions.append(functools.partial(func, data))

            with Pool(processes=10) as pool:
                pool.map(smap, functions)
