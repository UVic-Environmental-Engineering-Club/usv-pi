""" Functions that drive the boat """

import time
import math
import asyncio
from xmlrpc.client import boolean
import arrow


from src.data_classes.sensor.data_in import GpsCoord
from src.constants import SERIAL, DATA, GPS_COLLECTION, State, Gains, Error


def correct_rudder_angle(
    boat_heading: float, next_waypoint: float, delay_time: float
) -> None:
    """Corrects the rudder angle"""
    # Convert degrees to radians
    boat_heading = math.radians(boat_heading)
    next_waypoint = math.radians(next_waypoint)

    # Calculate the angle between the boat's heading and the next waypoint
    angle_diff = next_waypoint - boat_heading

    # Normalize the angle to be within -180 to 180 degrees
    if angle_diff > math.pi:
        angle_diff -= 2 * math.pi
    elif angle_diff < -math.pi:
        angle_diff += 2 * math.pi

    # Calculate the rudder angle to correct the course
    rudder_angle = math.degrees(
        math.atan2(2 * math.sin(angle_diff), 1 + math.cos(angle_diff))
    )
    SERIAL.write(rudder_angle)
    time.sleep(delay_time)


def correct_motor_power(
    distance: float, current_speed: float, delay_time: float
) -> None:
    """Corrects the motor power"""
    # Calculate the target speed based on the distance to the next waypoint
    target_speed = max(
        0, min(1, (distance / 100))
    )  # assuming a maximum distance of 100 meters

    # Calculate the difference between the current speed and the target speed
    speed_diff = target_speed - current_speed

    # Calculate the motor power adjustment
    motor_power = max(
        -1, min(1, speed_diff * 2)
    )  # assuming maximum power range of -1 to 1
    SERIAL.write(motor_power)
    time.sleep(delay_time)


async def driver_loop(iteration_time: int = 10):
    """Driver process logic lives in here"""
    # adjust rudder loop
    delay_time = 0.0005

    next_iteration = arrow.now().shift(seconds=iteration_time)

    current_point = DATA["route"].pop(0)
    db_usv_point = GPS_COLLECTION.find_one()
    usv_point = GpsCoord(arrow.now(), db_usv_point["long"], db_usv_point["lat"])
    correct_rudder_angle(
        get_heading(usv_point, current_point), current_point, delay_time
    )

    while True:
        await asyncio.sleep(0.5)
        if arrow.now() < next_iteration or DATA["state"] == State.COLLISION_DETECTION:
            continue

        next_iteration = arrow.now().shift(seconds=iteration_time)

        # Get most recent gps coordinate from database
        current_location = GPS_COLLECTION.find_one(sort=[("timestamp", -1)])



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


def is_threshold(
    current_location: GpsCoord, next_waypoint: GpsCoord, THRESHOLD: int
) -> bool:
    """Check if the current location is within the circumference of the next waypoint"""
    return get_distance(current_location, next_waypoint) < THRESHOLD
