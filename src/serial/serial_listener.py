""" Handles serial events"""

from src.events.event_type import EventType
from src.events.events import subscribe
from src.data_classes.sensor.data_in import SensorIn
from src.data_classes.sensor.data_out import SensorOut


def handle_serial_in(data: SensorIn):
    """Handles serial data in events"""
    pass


def handle_serial_out(data: SensorOut):
    """Handles serial data out events"""
    pass


def setup_serial_handlers():
    """Setup serial handlers for EventTypes"""
    subscribe(EventType.SERIAL_IN, handle_serial_in)
    subscribe(EventType.SERIAL_OUT, handle_serial_out)
