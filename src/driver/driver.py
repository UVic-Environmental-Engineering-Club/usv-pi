""" Functions that drive the boat """

from typing import List
from multiprocessing import Process
from src.data_classes.sensor.data_in import GpsCoord


def add_gps_coord(route: List[GpsCoord], coord: GpsCoord) -> List[GpsCoord]:
    """Adds a GpsCoord to the route"""
    pass


def remove_gps_coord(route: List[GpsCoord], coord: GpsCoord) -> List[GpsCoord]:
    """Removes a GpsCoord to the route"""
    pass


def reset_route() -> List[GpsCoord]:
    """Returns an empty list"""
    return []


def start_route(route: List[GpsCoord], start_target: GpsCoord) -> Process:
    """
    Starts a process (multiprocess from another core) to follow a route.
    Process will start from current location from start_target,
    start_target is in case it was paused previously
    """
    pass


def pause_route(route: List[GpsCoord]) -> GpsCoord:
    """Pauses the route and returns the node that it was currently going to"""
    pass
