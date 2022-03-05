""" Handles socketio events"""

from src.events.event_type import EventType
from src.events.events import subscribe
from src.events.events import post_event
from src.constants import SIO
from src.data_classes.socketio.message import Message
from src.serial.parse_input import parse_string

async def handle_serial_in(message: str):
    """Handles socketio data in events"""
           
    #send to socket
    await post_event(EventType.SOCKET_OUT, message)
    
    #send to database
    await post_event(EventType.DATABASE_WRITE, message)



async def handle_socketio_out(message: str):
    """Handles socketio data out events"""
     #deal with parsing functions
    
    parse_string('ACC-000-324-234')
   
    #send to socket
    await SIO.emit("serial", message, namespace="/usv")


def setup_socketio_handlers():
    """Setup socketio handlers for EventTypes"""
    subscribe(EventType.SERIAL_IN, handle_serial_in)
    subscribe(EventType.SOCKET_OUT, handle_socketio_out)
