import asyncio
from src.events.event_type import EventType
from src.events.events import post_event
from src.constants import SERIALccb #, SERIALpdb
""" Functions for things related to serial and pySerial """

async def serial_loop():
    await asyncio.sleep(1) 

    while True:
        await asyncio.sleep(0.001)
        if not SERIALccb : # or not SERIALpdb:
            print("Serial not initialized")
            continue

        try:
            # if SERIALpdb.is_open is True:
            #     message = SERIALpdb.readline().decode("utf8").strip()
            #     if message:
            #         await post_event(EventType.SERIAL_IN, message) 
            if SERIALccb.is_open is True:
                message = SERIALccb.readline().decode("utf8").strip()
                if message:
                    await post_event(EventType.SERIAL_IN, message)


        except Exception as e:
            print("Error reading from serial", e)
            break
