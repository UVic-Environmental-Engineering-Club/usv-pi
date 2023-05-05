""" Handles serial events"""

from src.events.event_type import EventType
from src.events.events import subscribe
from src.data_classes.sensor.data_out import SensorOut
from src.constants import SERIALccb
from src.events.events import post_event
from src.serial.parse_input import parse_string


async def handle_serial_in(message: str):
    """Handles socketio data in events"""
    parsed_serial_message = parse_string(message)

    if not parsed_serial_message:
        return

    # send to socket
    await post_event(EventType.SOCKET_OUT, parsed_serial_message)

    # send to database
    await post_event(EventType.DATABASE_WRITE, parsed_serial_message)


async def handle_serial_out(data: SensorOut):
    """Handles serial data out events"""
    if not SERIALccb:
        print("Serial not initialized")
        return

    try:
        if SERIALccb.is_open is True:
            SERIALccb.write(str.encode(data))
            print("sent to serial: " + data)
    except Exception as error:
        print("Error writing to serial", error)


def setup_serial_handlers():
    """Setup serial handlers for EventTypes"""
    subscribe(EventType.SERIAL_IN, handle_serial_in)
    subscribe(EventType.SERIAL_OUT, handle_serial_out)
