""" Contains all dataclasses for sensor data types from the micro controller """

from dataclasses import dataclass


@dataclass
class SensorIn:
    """Base SensorIn"""

    timestamp: int


@dataclass
class GpsCoord(SensorIn):
    """Dataclass for gps data"""

    longitude: float
    latitude: float
