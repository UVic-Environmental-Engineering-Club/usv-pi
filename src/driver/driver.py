""" Functions that drive the boat """

import math
import asyncio
from xmlrpc.client import boolean
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
    next_iteration = arrow.now().replace(second=0, microsecond=0).shift(seconds=10)
    current_point = DATA["route"].pop(0)
    db_usv_point = GPS_DATA_COLLECTION.find_one()
    usv_point = GpsCoord(arrow.now(), db_usv_point["long"], db_usv_point["lat"])

    while True:
        await asyncio.sleep(0.5)
        if arrow.now() < next_iteration:
            continue

        next_iteration = arrow.now().shift(seconds=iteration_time)
        next_iteration = arrow.now().replace(second=0, microsecond=0).shift(seconds=10)

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


def bound_detect(
    pt_p: GpsCoord, pt_a: GpsCoord, pt_b: GpsCoord, pt_c: GpsCoord
) -> boolean:
    """Using barycentric method to check wether a point is withing the bounds of a 2D triangle
    -> https://www.scratchapixel.com/lessons/3d-basic-rendering/ray-tracing-rendering-a-triangle/barycentric-coordinates#:~:text=Barycentric%20coordinates%20can%20be%20used%20to%20express%20the%20position%20of,the%20three%20triangle's%20vertices%20themselves.
    -> https://en.wikipedia.org/wiki/Barycentric_coordinate_system"""
    areal_coord_u = (pt_a.lat - pt_c.lat) * (pt_p.long - pt_c.long) - (
        pt_a.long - pt_c.long
    ) * (pt_p.lat - pt_c.lat)
    areal_coord_v = (pt_b.lat - pt_a.lat) * (pt_p.long - pt_a.long) - (
        pt_b.long - pt_a.long
    ) * (pt_p.lat - pt_a.lat)

    if (
        (areal_coord_u < 0) != (areal_coord_v < 0)
        and areal_coord_u != 0
        and areal_coord_v != 0
    ):
        return False

    areal_coord_w = (pt_c.lat - pt_b.lat) * (pt_p.long - pt_b.long) - (
        pt_c.long - pt_b.long
    ) * (pt_p.lat - pt_b.lat)
    return areal_coord_w == 0 or (areal_coord_w < 0) == (
        areal_coord_u + areal_coord_v <= 0
    )
