""" Handles socketio events"""

from src.events.event_type import EventType
from src.events.events import subscribe
from src.constants import SIO


async def handle_socketio_out(message: str):
    """Handles socketio data out events"""

    # send to socket
    await SIO.emit("serial", message, namespace="/usv")


def setup_socketio_handlers():
    """Setup socketio handlers for EventTypes"""
    subscribe(EventType.SOCKET_OUT, handle_socketio_out)
