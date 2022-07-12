""" Handles database events"""

from typing import Dict

from arrow import utcnow
from src.constants import (
    ACC_COLLECTION,
    BAT_COLLECTION,
    GPS_COLLECTION,
    GPSSTAT_COLLECTION,
    GYR_COLLECTION,
    LID_COLLECTION,
    MAG_COLLECTION,
    RPM_COLLECTION,
    TMP_COLLECTION,
    WET_COLLECTION,
)
from src.events.event_type import EventType
from src.events.events import subscribe


def get_collection_by_message_type(message_type: str):
    # print(message_type)
    if message_type == "ACC":
        return ACC_COLLECTION
    elif message_type == "GYR":
        return GYR_COLLECTION
    elif message_type == "MAG":
        return MAG_COLLECTION
    elif message_type == "LID":
        return LID_COLLECTION
    elif message_type == "BAT":
        return BAT_COLLECTION
    elif message_type == "RPM":
        return RPM_COLLECTION
    elif message_type == "TMP":
        return TMP_COLLECTION
    elif message_type == "WET":
        return WET_COLLECTION
    elif message_type == "GPS":
        return GPS_COLLECTION
    elif message_type == "GPSSTAT":
        return GPSSTAT_COLLECTION

    return None


async def handle_database_write(data: Dict[str, any]):
    """Handles database write events"""
    collection = get_collection_by_message_type(data["type"])
    if collection is None:
        return

    data["timestamp"] = utcnow().datetime
    collection.insert_one(data)


def setup_database_handlers():
    """Setup database for EventTypes"""
    subscribe(EventType.DATABASE_WRITE, handle_database_write)
