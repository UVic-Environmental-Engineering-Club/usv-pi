""" Functions for things related to serial and pySerial """

import time
from multiprocessing import Process


def init_serial_process() -> Process:
    """Returns the serial process"""

    return Process(target=serial_loop)


def serial_loop():
    """Serial loop with two threads, one for reading, one for writing"""
    """https://stackoverflow.com/questions/39127158/small-example-for-pyserial-using-threading"""
    while True:
        print("serial process!")
        time.sleep(2)
