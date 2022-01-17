from src.events.event_type import EventType
from src.events.events import post_event
import socketio


class USVNameSpace(socketio.AsyncClientNamespace):
    def on_connect(self):
        print("connected")
        pass

    def on_disconnect(self):
        print("disconnected")
        pass

    async def on_message(self, data):
        await post_event(EventType.SOCKET_IN, data)
