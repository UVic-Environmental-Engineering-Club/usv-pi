from src.constants import ROUTE, SHORE
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
        ROUTE.append(data)

    async def on_add_point_route_ack(self, data):
        print("add point route", data)
        ROUTE.append(data)
    
    async def on_add_point_shore_ack(self, data):
        print("add point shore", data)
        SHORE.append(data)

    async def on_delete_point_route_ack(self, data):
        print("delete point route", data)
        ROUTE.append(data)

    async def on_delete_point_shore_ack(self, data):
        print("delete point shore", data)
        SHORE.append(data)

    async def on_clear_route_ack(self, data):
        print("clear route", data)
        ROUTE.clear()

    async def on_clear_shore_ack(self, data):
        print("clear shore", data)
        SHORE.clear()
