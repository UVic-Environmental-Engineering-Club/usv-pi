""" Handles serial events"""

from src.events.event_type import EventType
from src.events.events import subscribe
from src.data_classes.sensor.data_in import SensorIn
from src.data_classes.sensor.data_out import SensorOut
from src.constants import SERIAL


async def handle_serial_in(data: SensorIn):
    """Handles serial data in events"""
    print("serial in")
    pass


async def handle_serial_out(data: SensorOut):
    """Handles serial data out events"""
    if not SERIAL:
         print("Serial not initialized")
    try:
         if SERIAL.is_open == True:
            SERIAL.write(str.encode(data))
            print("sent to serial: " + data )
    except:
        print("Error writing to serial")



def setup_serial_handlers():
    """Setup serial handlers for EventTypes"""
    subscribe(EventType.SERIAL_IN_GPS, handle_serial_in)
    subscribe(EventType.SERIAL_OUT, handle_serial_out)
