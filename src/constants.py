import asyncio
import json
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from pymongo import MongoClient

import socketio
from serial import Serial
from src.data_classes.sensor.data_in import GpsCoord
from src.events.event_type import EventType

PORT = serial.Serial("/dev/cu.usbserial-0001", 115200, timeout=0.5)


SERIAL: Optional[Serial] = None
MONGO_CLIENT: Optional[MongoClient] = None


class State(Enum):
    """States for the USV"""

    STOP = auto()
    DRIVE = auto()
    COLLISION_DETECTION = auto()
    SHORE_DETECTION = auto()
    EMERGENCY = auto()
    ADJUST_RUDDERS = auto()
    GO_TO_POINT = auto()


with open(file="config.json", mode="r", encoding="utf-8") as file:
    config = json.load(file)
    env = config["env"]

    try:
        SERIAL = Serial(config["port"], config["baudrate"], timeout=config["timeout"])
    except Exception as error:
        print("Could not open serial port.", error)
        SERIAL = None

    try:
        if env == "dev":
            MONGO_CLIENT = MongoClient(
                config["mongo_url_dev"].replace(
                    "<password>", config["mongo_dev_password"]
                )
            )
        else:
            MONGO_CLIENT = MongoClient(config["mongo_url_prod"])

    except Exception as error:
        print("Could not open database.", error)
        MONGO_CLIENT = None

DATA: Dict[str, Union[State, List[GpsCoord]]] = {
    "state": State,
    "route": [],
    "shore": [],
}
SUBSCRIBERS: Dict[EventType, List[Callable[[Any], Any]]] = {}
EVENT_LIST: asyncio.Queue[Tuple[EventType, Any]] = asyncio.Queue()

SIO = socketio.AsyncClient()

SENSOR_NAMES = (
    "ACC",
    "GYR",
    "MAG",
    "LID",
    "BAT",
    "RPM",
    "TMP",
    "WET",
    "GPS",
    "GPSSTAT",
)

DATABASE_NAMES = (
    "accelerometer_data",
    "gyroscope_data",
    "magnetometer_data",
    "lidar_data",
    "battery_data",
    "rpm_data",
    "temperature_data",
    "wet_data",
    "gps_data",
    "gps_stats_data",
)

USV_DB = MONGO_CLIENT.usv
for database_name in DATABASE_NAMES:
    if database_name not in USV_DB.list_collection_names():
        USV_DB.command(
            "create",
            database_name,
            timeseries={
                "timeField": "timestamp",
                "metaField": "data",
                "granularity": "seconds",
            },
        )

ACC_COLLECTION = USV_DB.accelerometer_data
GYR_COLLECTION = USV_DB.gyroscope_data
MAG_COLLECTION = USV_DB.magnetometer_data
LID_COLLECTION = USV_DB.lidar_data
BAT_COLLECTION = USV_DB.battery_data
RPM_COLLECTION = USV_DB.rpm_data
TMP_COLLECTION = USV_DB.temperature_data
WET_COLLECTION = USV_DB.wet_data
GPS_COLLECTION = USV_DB.gps_data
GPSSTAT_COLLECTION = USV_DB.gps_stats_data
