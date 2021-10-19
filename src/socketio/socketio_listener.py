""" Handles socketio events"""

from multiprocessing import Manager
from typing import Dict, Callable, Any, List
from src.events.event_type import EventType
from src.events.events import subscribe
from src.data_classes.socketio.message import Message


def handle_socketio_in(message: Message):
    """Handles socketio data in events"""
    pass


def handle_socketio_out(message: Message):
    """Handles socketio data out events"""
    pass


def setup_socketio_handlers(
    manager: Manager, subscribers: Dict[EventType, List[Callable[[Any], Any]]]
):
    """Setup socketio handlers for EventTypes"""
    subscribe(manager, subscribers, EventType.SOCKET_IN, handle_socketio_in)
    subscribe(manager, subscribers, EventType.SOCKET_OUT, handle_socketio_out)
