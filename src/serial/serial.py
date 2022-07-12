""" Functions for things related to serial and pySerial """
import asyncio
from src.events.event_type import EventType
from src.events.events import post_event
from src.constants import SERIAL


async def serial_loop():
    """Serial loop with two threads, one for reading, one for writing"""
    """https://stackoverflow.com/questions/39127158/small-example-for-pyserial-using-threading"""
    await asyncio.sleep(1)

    while True:
        await asyncio.sleep(0.001)
        if not SERIAL:
            print("Serial not initialized")
            continue

        try:
            if SERIAL.is_open == True:
                message = SERIAL.readline().decode("utf8").strip()
                if message:
                    await post_event(EventType.SERIAL_IN, message)

        except Exception as e:
            print("Error reading from serial", e)
            break
