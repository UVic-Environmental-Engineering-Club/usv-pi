""" Enum types for events """

from enum import Enum, auto


class EventType(Enum):
    """Enum types for events"""

    SOCKET_IN = auto()
    SOCKET_OUT = auto()
    DATABASE_WRITE = auto()
    DATABASE_READ = auto()

    SERIAL_IN_MAGNETOMETER = auto()
    SERIAL_IN_GPS = auto()
    SERIAL_IN_ACCELEROMETER = auto()
    SERIAL_IN_BATTERY = auto()

    SERIAL_OUT = auto()
