""" Main loop that is run on the Raspberry Pi on the USV 🛳⚓️ """

from typing import List, Optional
from serial import Serial
from src.data_classes.sensor.data_in import GpsCoord

serial: Optional[Serial] = None
route: List[GpsCoord] = []


def run():
    """Used to start the loop in __main__"""
    print("hello world!")
