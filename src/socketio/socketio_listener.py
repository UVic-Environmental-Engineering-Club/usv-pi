""" Handles socketio events"""

from src.events.event_type import EventType
from src.events.events import subscribe
from src.data_classes.socketio.message import Message


async def handle_socketio_in(message: Message):
    """Handles socketio data in events"""
    print("handle socket in message:", message)
    pass


async def handle_socketio_out(message: Message):
    """Handles socketio data out events"""
    pass


def setup_socketio_handlers():
    """Setup socketio handlers for EventTypes"""
    subscribe(EventType.SOCKET_IN, handle_socketio_in)
    subscribe(EventType.SOCKET_OUT, handle_socketio_out)
