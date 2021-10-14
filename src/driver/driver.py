""" Functions that drive the boat """

import time
from typing import List
from multiprocessing import Process
from src.data_classes.sensor.data_in import GpsCoord


def init_driver_process() -> Process:
    """Returns the driver process"""

    return Process(target=driver_loop)


def driver_loop():
    """Driver process logic lives in here"""
    while True:
        print("driver process!")
        time.sleep(2)


def add_gps_coord(route: List[GpsCoord], coord: GpsCoord) -> List[GpsCoord]:
    """Adds a GpsCoord to the route"""
    return route.append(coord)

def remove_gps_coord(route: List[GpsCoord], coord: GpsCoord) -> List[GpsCoord]:
    """Removes a GpsCoord to the route"""
    return route.remove(coord)


def reset_route() -> List[GpsCoord]:
    """Returns an empty list"""
    return []


def start_route(route: List[GpsCoord], start_target: GpsCoord) -> Process:
    """
    Starts a process (multiprocess from another core) to follow a route.
    Process will start from current location from start_target,
    start_target is in case it was paused previously
    """
    return init_driver_process()


def pause_route(route: List[GpsCoord]) -> GpsCoord:
    """Pauses the route and returns the node that it was currently going to"""
    pass
