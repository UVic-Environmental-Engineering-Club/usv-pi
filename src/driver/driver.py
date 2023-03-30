""" Functions that drive the boat """

import math
import asyncio
from xmlrpc.client import boolean
import arrow
import utm

from src.data_classes.sensor.data_in import GpsCoord
from src.constants import DATA, GPS_COLLECTION, State


def turn_left():
    print("turn left")
    return


def turn_right():
    print("turn right")
    return


def forward():
    print("going forward")
    return


async def driver_loop(iteration_time: int = 10):
    """Driver process logic lives in here"""
    # adjust rudder loop
    next_iteration = arrow.now().shift(seconds=iteration_time)

    current_point = DATA["route"].pop(0)
    db_usv_point = GPS_COLLECTION.find_one()
    usv_point = GpsCoord(arrow.now(), db_usv_point["long"], db_usv_point["lat"])

    while True:
        await asyncio.sleep(0.5)
        if arrow.now() < next_iteration or DATA["state"] == State.COLLISION_DETECTION:
            continue

        next_iteration = arrow.now().shift(seconds=iteration_time)

        # Get most recent gps coordinate from database
        current_location = GPS_COLLECTION.find_one(sort=[("timestamp", -1)])


def boundary_calc(pt_a: GpsCoord, pt_b: GpsCoord) -> tuple[GpsCoord, GpsCoord]:
    """Calculate the boundary"""
    pt_c = GpsCoord(arrow.now(), 0, 0)
    pt_d = GpsCoord(arrow.now(), 0, 0)

    slope = (pt_b.long - pt_a.long) / (pt_b.lat - pt_a.lat)

    dy = math.sqrt(3**2 / (slope**2 + 1))
    dx = -slope * dy

    pt_c.lat = pt_b.lat + dx
    pt_c.long = pt_b.long + dy
    pt_d.lat = pt_b.lat - dx
    pt_d.long = pt_b.long - dy

    return (pt_c, pt_d)


def bound_detect(
    pt_p: GpsCoord, pt_a: GpsCoord, pt_b: GpsCoord, pt_c: GpsCoord
) -> boolean:
    """Using barycentric method to check wether a point is within the bounds of a 2D triangle
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


def geographic_to_UTM(point: GpsCoord) -> tuple[float, float, float]:
    """Converts a point from geographic coordinates to UTM coordinates"""
    return utm.from_latlon(point.lat, point.long)


def heading(x, y) -> float:
    """This formula gives the direction of the (x, y) vector counted clockwise from the y axis.
    The correct formula depends then on how the magnetometer has been mounted relative to the vehicle.
    If we assume that the x axis of the magnetometer points forward and the y axis points to the left, then:

    - the vehicle is heading north (0° magnetic heading) when the horizontal component of the magnetic field is along +x
    - the vehicle is heading east (90° magnetic heading) when the horizontal component of the magnetic field is along +y

    NOTE: Magnetic declination has to be added if one is interested in the true (rather than magnetic) heading.
    -> https://arduino.stackexchange.com/questions/18625/converting-three-axis-magnetometer-to-degrees/88707#88707"""
    return math.atan2(y, x) * 180 / math.pi


def geographic_to_cartesian(point: GpsCoord) -> tuple[float, float, float]:
    """Converts a point from geographic coordinates to cartesian coordinates"""
    x = math.cos(point.lat) * math.cos(point.long)
    y = math.cos(point.lat) * math.sin(point.long)
    z = math.sin(point.lat)

    return (x, y, z)


def get_bearing(point_a: GpsCoord, point_b: GpsCoord) -> float:
    """Calculate the bearing between two points"""
    x = math.sin(point_b.long - point_a.long) * math.cos(point_b.lat)
    y = math.cos(point_a.lat) * math.sin(point_b.lat) - math.sin(
        point_a.lat
    ) * math.cos(point_b.lat) * math.cos(point_b.long - point_a.long)
    return math.atan2(x, y)


def get_heading(point_a: GpsCoord, point_b: GpsCoord) -> float:
    """Calculate the heading between two points"""
    return math.atan2(point_b.long - point_a.long, point_b.lat - point_a.lat)


def get_rudder_angle(point_a: GpsCoord, point_b: GpsCoord) -> float:
    """Calculate the rudder angle between two points"""
    return (
        math.atan2(point_b.long - point_a.long, point_b.lat - point_a.lat)
        * 180
        / math.pi
    )


def get_distance(point_a: GpsCoord, point_b: GpsCoord) -> float:
    """Calculate the distance between two points"""
    return math.sqrt(
        (point_a.lat - point_b.lat) ** 2 + (point_a.long - point_b.long) ** 2
    )
