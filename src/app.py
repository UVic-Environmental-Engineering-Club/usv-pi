""" Main loop that is run on the Raspberry Pi on the USV 🛳⚓️ """
import asyncio

from src.collision_detection.collision_detection import collision_detection_loop
from src.constants import SIO
from src.database.database_listener import setup_database_handlers
from src.driver.driver import driver_loop
from src.events.event_type import EventType
from src.events.events import post_event, run_event_loop
from src.serial.serial import serial_loop
from src.serial.serial_listener import setup_serial_handlers
from src.socketio.namespace import USVNameSpace
from src.socketio.socketio_listener import setup_socketio_handlers


async def test():
    while True:
        await asyncio.sleep(1)
        await post_event(EventType.SERIAL_OUT, "mr100")
        await post_event(EventType.SERIAL_OUT, "ml050")


async def run():
    """Used to start the loop in __main__"""
    setup_database_handlers()
    setup_serial_handlers()
    setup_socketio_handlers()

    SIO.register_namespace(USVNameSpace("/usv"))

    try:
        await SIO.connect("http://localhost:8080/")
    except Exception as error:
        print("Could not open socket.io connection.", error)

    coroutines = []

    coroutines.append(asyncio.create_task(driver_loop()))
    coroutines.append(asyncio.create_task(serial_loop()))
    coroutines.append(asyncio.create_task(run_event_loop()))
    coroutines.append(asyncio.create_task(collision_detection_loop()))

    await asyncio.gather(*coroutines)
