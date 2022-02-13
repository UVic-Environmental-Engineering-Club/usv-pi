""" Handles database events"""

from multiprocessing import Manager
from typing import Dict, Callable, Any, List
from src.events.event_type import EventType
from src.events.events import subscribe


async def handle_database_write(data : str):
    """Handles database write events"""
    print("data write " + data)
    


async def handle_database_read():
    """Handles database read events"""
    print("data read")
    pass


def setup_database_handlers():
    """Setup database for EventTypes"""
    subscribe(EventType.DATABASE_WRITE, handle_database_write)
    subscribe(EventType.DATABASE_READ, handle_database_read)
