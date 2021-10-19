""" Functions for things related to serial and pySerial """

import time
from typing import List, Tuple, Any
from src.events.event_type import EventType


def serial_loop(event_list: List[Tuple[EventType, Any]]):
    """Serial loop with two threads, one for reading, one for writing"""
    """https://stackoverflow.com/questions/39127158/small-example-for-pyserial-using-threading"""
    while True:
        print("serial process!")
        time.sleep(2)
