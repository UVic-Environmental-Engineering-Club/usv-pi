""" Enum types for events """

from enum import Enum


class EventType(Enum):
    """Enum types for events"""

    WEBSOCKET_IN = 1
    WEBSOCKET_OUT = 2
    DATABASE_WRITE = 3
    DATABASE_READ = 4
