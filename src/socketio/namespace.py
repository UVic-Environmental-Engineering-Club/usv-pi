from src.constants import DATA
import socketio


class USVNameSpace(socketio.AsyncClientNamespace):
    def on_connect(self):
        print("connected")
        pass

    def on_disconnect(self):
        print("disconnected")
        pass

    async def on_update_route_ack(self, data):
        DATA["route"] = data

    async def on_update_shore_ack(self, data):
        DATA["shore"] = data