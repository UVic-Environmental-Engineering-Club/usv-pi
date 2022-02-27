""" Handles serial events"""

from src.socketio.socketio_listener import handle_socketio_out
from src.events.event_type import EventType
from src.events.events import subscribe
from src.data_classes.sensor.data_in import SensorIn
from src.data_classes.sensor.data_out import SensorOut
from src.constants import SERIAL
from src.events.events import post_event



async def handle_serial_out(data: SensorIn):
    """Handles serial data in events"""
    
    ##send to socket
    await post_event(EventType.SOCKET_OUT, data)
    


async def handle_socketio_in(data: SensorOut):
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
    subscribe(EventType.SERIAL_OUT, handle_serial_out)
    subscribe(EventType.SOCKET_IN, handle_socketio_in)
