from src.constants import ROUTE
import socketio


class USVNameSpace(socketio.AsyncClientNamespace):
    def on_connect(self):
        print("connected")
        pass

    def on_disconnect(self):
        print("disconnected")
        pass

    async def on_init_route(self, data):
        print("init route", data)
        ROUTE = data

    async def on_add_point_ack(self, data):
        print(data)

    async def on_delete_point_ack(self, data):
        print(data)

    async def on_clear_route_ack(self, data):
        print(data)
