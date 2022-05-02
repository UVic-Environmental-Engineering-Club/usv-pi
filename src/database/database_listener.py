""" Handles database events"""

from typing import Dict
from arrow import utcnow
from src.constants import SENSOR_DATA_COLLECTION
from src.events.event_type import EventType
from src.events.events import subscribe


async def handle_database_write(data: Dict[str, any]):
    """Handles database write events"""
    SENSOR_DATA_COLLECTION.insert_one(
        {"timestamp": utcnow().datetime, "type": data["type"], "data": data["data"]}
    )


async def handle_database_read():
    """Handles database read events"""
    print("data read")
    pass


def setup_database_handlers():
    """Setup database for EventTypes"""
    subscribe(EventType.DATABASE_WRITE, handle_database_write)
    subscribe(EventType.DATABASE_READ, handle_database_read)
