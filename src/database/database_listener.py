""" Handles database events"""


from src.events.event_type import EventType
from src.events.events import subscribe


def handle_database_write():
    """Handles database write events"""
    pass


def handle_database_read():
    """Handles database read events"""
    pass


def setup_database_handlers():
    """Setup database for EventTypes"""
    subscribe(EventType.DATABASE_WRITE, handle_database_write)
    subscribe(EventType.DATABASE_READ, handle_database_read)
