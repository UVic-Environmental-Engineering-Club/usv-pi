""" Main loop that is run on the Raspberry Pi on the USV 🛳⚓️ """

from typing import List, Optional
from multiprocessing import Process
from serial import Serial
from src.data_classes.sensor.data_in import GpsCoord

serial: Optional[Serial] = None

route: List[GpsCoord] = []
paused_gps_coord: Optional[GpsCoord] = None
driver_process: Optional[Process] = None

with open(file="config.json", mode="r", encoding="utf-8") as file:
    pass


def run():
    """Used to start the loop in __main__"""
    print("hello world!")
