""" Handles database events"""

from multiprocessing import Manager
from typing import Dict, Callable, Any, List
from src.events.event_type import EventType
from src.events.events import subscribe


def handle_database_write():
    """Handles database write events"""
    pass


def handle_database_read():
    """Handles database read events"""
    pass


def setup_database_handlers(
    manager: Manager, subscribers: Dict[EventType, List[Callable[[Any], Any]]]
):
    """Setup database for EventTypes"""
    subscribe(manager, subscribers, EventType.DATABASE_WRITE, handle_database_write)
    subscribe(manager, subscribers, EventType.DATABASE_READ, handle_database_read)
