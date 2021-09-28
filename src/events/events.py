""" Subscriber/Observer programming paradigm """

from typing import Dict, List, Any
from collections.abc import Callable
from src.events.event_type import EventType

subscribers: Dict[EventType, List[Callable[[Any], Any]]] = []


def subscribe(event: EventType, func: Callable[[Any], Any]):
    """Adds an EventType and observer function to subscribers"""
    pass


def post_event(event: EventType, data: Any):
    """Runs all observer functions for the EventType"""
    pass
