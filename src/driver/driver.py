""" Functions that drive the boat """

import math
import asyncio
import arrow

from src.data_classes.sensor.data_in import GpsCoord
from src.constants import DATA, GPS_DATA_COLLECTION


async def driver_loop(iteration_time: int = 10):
    """Driver process logic lives in here"""
    # adjust rudder loop
    next_iteration = arrow.now().shift(seconds=iteration_time)

    current_point = DATA["route"].pop(0)
    db_usv_point = GPS_DATA_COLLECTION.find_one()
    usv_point = GpsCoord(arrow.now(), db_usv_point["long"], db_usv_point["lat"])
    print(boundary_calc(usv_point, current_point))

    while True:
        await asyncio.sleep(0.5)
        if arrow.now() < next_iteration:
            continue

        next_iteration = arrow.now().shift(seconds=iteration_time)

        # Get most recent gps coordinate from database
        current_location = GPS_DATA_COLLECTION.find().limit(1).sort({"$natural": -1})


def boundary_calc(point_a: GpsCoord, point_b: GpsCoord) -> tuple[GpsCoord, GpsCoord]:
    """Calculate the boundary"""
    c = GpsCoord(arrow.now(), 0, 0)
    d = GpsCoord(arrow.now(), 0, 0)

    slope = (point_b.long - point_a.long) / (point_b.lat - point_a.lat)

    dy = math.sqrt(3**2 / (slope**2 + 1))
    dx = -slope * dy

    c.lat = point_b.lat + dx
    c.long = point_b.long + dy
    d.lat = point_b.lat - dx
    d.long = point_b.long - dy

    return (c, d)
