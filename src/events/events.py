""" Subscriber/Observer programming paradigm """

import functools
from multiprocessing import Pool
from multiprocessing.context import Process
from typing import Dict, List, Any, Tuple
from collections.abc import Callable
from src.events.event_type import EventType

subscribers: Dict[EventType, List[Callable[[Any], Any]]] = {}
event_list: List[Tuple[EventType, Any]] = []


def subscribe(event: EventType, func: Callable[[Any], Any]) -> None:
    """Adds an EventType and observer function to subscribers"""
    if not event in subscribers:
        subscribers[event] = []
    subscribers[event].append(func)


def post_event(event: EventType, data: Any) -> None:
    """Runs all observer functions for the EventType"""
    event_list.append((event, data))


def smap(func) -> Callable[[Any], Any]:
    """Helper function that returns function thats passed in"""
    return func()


def run_event_loop():
    """Infinite loop for running event loop"""
    while True:
        if len(event_list) != 0:
            functions: List[Process] = []

            [event_type, data] = event_list.pop()
            for func in subscribers[event_type]:
                functions.append(functools.partial(func, data))

            with Pool(processes=10) as pool:
                pool.map(smap, functions)
