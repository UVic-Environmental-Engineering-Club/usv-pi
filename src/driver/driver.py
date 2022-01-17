""" Functions that drive the boat """

import asyncio
from typing import List
from src.data_classes.sensor.data_in import GpsCoord


async def driver_loop():
    """Driver process logic lives in here"""
    while True:
        print("driver process!")
        await asyncio.sleep(2)


def add_gps_coord(route: List[GpsCoord], coord: GpsCoord) -> List[GpsCoord]:
    """Adds a GpsCoord to the route"""
    return route + [coord]


def remove_gps_coord(route: List[GpsCoord], coord: GpsCoord) -> List[GpsCoord]:
    """Removes a GpsCoord to the route"""
    return [curCoord for curCoord in route if curCoord != coord]


def reset_route() -> List[GpsCoord]:
    """Returns an empty list"""
    return []


def start_route(route: List[GpsCoord], start_target: GpsCoord) -> None:
    """
    Starts a process (multiprocess from another core) to follow a route.
    Process will start from current location from start_target,
    start_target is in case it was paused previously
    """
    pass


def pause_route(route: List[GpsCoord]) -> GpsCoord:
    """Pauses the route and returns the node that it was currently going to"""
    pass
