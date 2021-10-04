""" Enum types for events """

from enum import Enum


class EventType(Enum):
    """Enum types for events"""

    SOCKET_IN = 1
    SOCKET_OUT = 2
    DATABASE_WRITE = 3
    DATABASE_READ = 4
    SERIAL_IN = 5
    SERIAL_OUT = 5
