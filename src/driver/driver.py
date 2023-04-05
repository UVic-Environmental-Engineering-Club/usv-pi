""" Functions that drive the boat """

import time
import math
import asyncio
from xmlrpc.client import boolean
import arrow
import utm


from src.data_classes.sensor.data_in import GpsCoord
from src.constants import PORT, DATA, GPS_COLLECTION, State, Gains, Error


def update_rudder_angle(old_angle: float, new_angle: float, delay_time: float) -> None:
    """Updates the rudder angle"""

    # delay time is how to control the speed the servo will change angles

    # make the servo change from old to new degrees in increments, not all at once
    if new_angle > old_angle:
        for signal in range(old_angle, new_angle + 1, 1):
            # in steps of 1 degree
            PORT.write(signal)
            time.sleep(delay_time)

    if new_angle < old_angle:
        for signal in range(old_angle, new_angle - 1, -1):
            # in steps of 1 degree
            PORT.write(signal)
            time.sleep(delay_time)


def update_motor_power(old_power: float, new_power: float, delay_time: float) -> None:
    """Updates the motor speed"""

    # delay time is how to control the speed the motor will change power

    # make the motor change from old to new power in increments, not all at once
    if new_power > old_power:
        for signal in range(old_power, new_power + 1, 1):
            # in steps of 1 perent
            PORT.write(signal)
            time.sleep(delay_time)

    if new_power < old_power:
        for signal in range(old_power, new_power - 1, -1):
            # in steps of 1 percent
            PORT.write(signal)
            time.sleep(delay_time)


async def driver_loop(iteration_time: int = 10):
    """Driver process logic lives in here"""
    # adjust rudder loop
    delay_time = 0.0005
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


def is_threshold(
    current_location: GpsCoord, next_waypoint: GpsCoord, THRESHOLD: int
) -> bool:
    """Check if the current location is within the circumference of the next waypoint"""
    return get_distance(current_location, next_waypoint) < THRESHOLD


def pid(
    val: float,
    set_point: float,
    upper_lim: float,
    lower_lim: float,
) -> float:
    """PID controller"""
    error = set_point - val

    p_value = error * Gains.K_P.value
    i_value = Error.CUMULATIVE.value * Gains.K_I.value
    d_value = (error - Error.PREVIOUS.value) * Gains.K_D.value

    pid_value = p_value + i_value + d_value

    Error.CUMULATIVE.value += error
    Error.PREVIOUS.value = error
    val_range = upper_lim - lower_lim
    new_val = map(pid_value, -1 * val_range, val_range, lower_lim, upper_lim)

    if new_val > upper_lim:
        new_val = upper_lim

    if new_val < lower_lim:
        new_val = lower_lim

    return new_val
