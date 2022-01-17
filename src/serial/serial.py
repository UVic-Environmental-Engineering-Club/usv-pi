""" Functions for things related to serial and pySerial """
import asyncio
from src.constants import SERIAL


async def serial_loop():
    """Serial loop with two threads, one for reading, one for writing"""
    """https://stackoverflow.com/questions/39127158/small-example-for-pyserial-using-threading"""

    while True:
        print("serial process!")
        await asyncio.sleep(2)
        if not SERIAL:
            print("Serial not initialized")
            continue

        try:
            if SERIAL.is_open == True:
                print(SERIAL.read())
        except:
            print("Error reading from serial")
            break
