""" Contains all dataclasses for sensor data types from the micro controller """

from dataclasses import dataclass

from arrow import Arrow


@dataclass
class SensorIn:
    """Base SensorIn"""

    timestamp: Arrow


@dataclass
class GpsCoord(SensorIn):
    """Dataclass for gps data"""

    long: float
    lat: float
